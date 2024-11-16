import asyncio
from app.openai_service.event_handler.enhanced_event_handler import EnhancedExplanationEventHandler

from app.openai_service.event_handler.explanation_event_handler import ExplanationEventHandler
from app.openai_service.event_handler.feedback_event_handler import FeedbackEventHandler
from app.openai_service.event_handler.index_event_handler import IndexEventHandler
from app.openai_service.assistant_api_utils import *
from app.message_processor.instructions.beginner_instructions import *


async def load_prompt(prompt_key, **kwargs):
    with open("app/message_processor/instructions/prompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
    prompt_template = prompts.get(prompt_key, {}).get("prompt", "")

    # format the prompt with the given keyword arguments
    formatted_prompt = prompt_template.format(**kwargs)
    return formatted_prompt

async def read_text_file(file_path: str) -> str:
    """
    주어진 경로의 텍스트 파일을 읽어 내용을 문자열로 반환.

    Parameters:
        file_path (str): 읽을 텍스트 파일의 경로

    Returns:
        str: 파일의 내용
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return ""
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return ""

async def read_and_format_text_file(file_path: str, **kwargs) -> str:
    """
    주어진 경로의 텍스트 파일을 읽어와서 지정된 키워드 인자(**kwargs)를 사용해 포맷팅된 문자열을 반환합니다.

    Parameters:
        file_path (str): 읽을 텍스트 파일의 경로
        **kwargs: 포맷팅에 사용할 키워드 인자들 (예: request_id='12345', index_id='1')

    Returns:
        str: 포맷팅된 파일의 내용
    """
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            template_content = file.read()

        # 포맷팅
        formatted_content = template_content.format(**kwargs)
        return formatted_content

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return ""
    except KeyError as e:
        print(f"포맷팅 중 오류 발생: 필요한 키 값이 없습니다 - {e}")
        return ""
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return ""

class MessageProcessor:
    def __init__(self, request_id, assistant, explanation_level, producer):
        self.request_id = request_id
        self.total_chunks = None
        self.assistant = assistant
        self.explanation_level = explanation_level
        self.producer = producer


    async def initiate(self, file_path: str):

        vector_store = await create_vector_store()
        logger.info(f"Vector store 생성: {vector_store.id}")

        #file_batch = await add_file_to_vector_store(vector_store_id=vector_store.id,file_path=file_path)
        #logger.info(f"Text file upload 완료: {file_batch.id}")

        #thread = await create_thread_with_vector_store(vector_store)
        thread = await create_thread()
        logger.info(f"Thread 생성: {thread.id}")
        return thread, vector_store

    async def create_indices(self, thread):
        logger.info(f"목차 생성 시작 | Thread ID: {thread.id}")

        instruction = load_create_index_prompt(self.request_id)
        text = await read_text_file("capstone_storage/test_request_123/original_test_request_123.txt")
        instruction+=text
        run = await run_stream(self.assistant.id, thread.id, event_handler=IndexEventHandler(self.request_id, producer=self.producer), instructions=instruction)


    async def create_explanations(self, dir_path):
        logger.info("설명문 생성 시작 - 분할된 텍스트 파일들 병렬 처리")

        chunk_files = os.listdir(dir_path)
        self.total_chunks = len(chunk_files)
        """
        tasks = [
            self.create_chunk_explanation(os.path.join(dir_path, chunk_file_name), idx, request_id=self.request_id)
            for idx, chunk_file_name in enumerate(chunk_files, start=1)
        ]
        """
        tasks = [
            asyncio.create_task(
                self.create_chunk_explanation(os.path.join(dir_path, chunk_file_name), idx, request_id=self.request_id)
            )
            for idx, chunk_file_name in enumerate(chunk_files, start=1)
        ]

        results = await asyncio.gather(*tasks)
        logger.info("모든 설명문 생성 작업이 완료되었습니다.")
        return results

    # 병렬적으로 수행하기 위해 create explanation으로 asyncio로 thread를 개수만큼 바로 생성하고 요구를  보내도록 수정하기
    async def create_chunk_explanation(self, chunk_file_path, chunk_index, request_id):
        #thread, vector_store = await self.initiate(chunk_file_path)
        thread = await create_thread()
        event_handler = ExplanationEventHandler(
             request_id=self.request_id, chunk_index=chunk_index
        )

        logger.info(f"설명문 생성 시작 | 파일: {chunk_file_path} | Thread ID: {thread.id} | 청크: {chunk_index + 1}/{self.total_chunks}")

        instruction = create_explanation.format(request_id=request_id, index_id=chunk_index)
        chunk_text = await read_text_file(f"capstone_storage/{request_id}/transcription_chunks/{request_id}_{chunk_index}.txt")
        instructions = instruction+chunk_text

        await run_stream(self.assistant.id, thread.id, event_handler=event_handler, instructions=instructions
        )

        logger.info(f"설명문 생성 완료 | Thread ID: {thread.id} | 청크: {chunk_index}/{self.total_chunks}")
        return thread

    async def create_feedbacks_for_explanations(self, results):
        logger.info("피드백 텍스트 병렬 생성 시작")
        tasks = [self.create_chunk_feedback(thread, chunk_index=idx, request_id=self.request_id) for idx, thread in
                 enumerate(results, start=1)]
        await asyncio.gather(*tasks)
        logger.info("모든 피드백 생성 작업이 완료되었습니다.")

    async def create_chunk_feedback(self, thread, chunk_index, request_id):
        feedback_event_handler = FeedbackEventHandler(
            thread_id=thread.id,  request_id=self.request_id, chunk_index=chunk_index
        )

        logger.info(f"피드백 생성 시작 | Thread ID: {thread.id} | 청크: {chunk_index}/{self.total_chunks}")
        instruction = create_feedback.format(request_id=request_id, chunk_index=chunk_index)
        chunk_explanation_text = await read_text_file(f"capstone_storage/{request_id}/explanation/explanation_{request_id}_{chunk_index}.txt")
        chunk_text = await read_text_file(f"capstone_storage/{request_id}/transcription_chunks/{request_id}_{chunk_index}.txt")
        instructions = instruction+chunk_explanation_text+"\n\n original_text: "+chunk_text

        logger.info("instruction 생성완료")
        await run_stream(self.assistant.id, thread.id, event_handler=feedback_event_handler, instructions=instructions)

        logger.info(f"피드백 생성 완료 | Thread ID: {thread.id} | 청크: {chunk_index}/{self.total_chunks}")

    async def create_enhanced_explanations(self, results):
        logger.info("피드백 반영 설명문 텍스트 병렬 생성 시작")
        tasks = [self.create_enhanced_chunk_explanation(thread, idx) for idx, thread in
                 enumerate(results,start=1)]

        await asyncio.gather(*tasks)
        logger.info("모든 피드백 반영 설명문 생성 작업이 완료되었습니다.")


    async def create_enhanced_chunk_explanation(self, thread, chunk_index):
        enhanced_explanation_event_handler = EnhancedExplanationEventHandler(
            thread_id=thread.id, request_id=self.request_id, chunk_index=chunk_index, kafka_producer=self.producer
        )

        logger.info(f"피드백 반영 설명문 생성 시작 | Thread ID: {thread.id} | 청크: {chunk_index}/{self.total_chunks}")

        instruction = create_enhanced_explanation
        chunk_explanation_text = await read_text_file(f"capstone_storage/{self.request_id}/explanation/explanation_{self.request_id}_{chunk_index}.txt")
        chunk_explanation_feedback_text = await read_text_file(f"capstone_storage/{self.request_id}/feedback/feedback_{self.request_id}_{chunk_index}.txt")
        instructions = instruction+chunk_explanation_text+"\n\n feedback of the explanation: "+chunk_explanation_feedback_text
        await run_stream(self.assistant.id, thread.id, event_handler=enhanced_explanation_event_handler, instructions=instructions)

        logger.info(f"피드백 반영 설명문 생성 완료 | Thread ID: {thread.id} | 청크: {chunk_index}/{self.total_chunks}")

