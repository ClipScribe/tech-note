import asyncio


from app.openai_service.event_handler.enhandced_event_handler import EnhancedExplanationEventHandler
from app.openai_service.event_handler.explanation_event_handler import ExplanationEventHandler
from app.openai_service.event_handler.feedback_event_handler import FeedbackEventHandler
from app.openai_service.event_handler.index_event_handler import IndexEventHandler
from app.openai_service.assistant_api_utils import *

# 로그 형식 통일 설정
logger.add(
    "file_{time}.log",  # 로그 파일 이름 형식
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | Request ID: {extra[request_id]} | {message}",
    level="INFO",
)


class MessageProcessor:
    def __init__(self, request_id, assistant, explanation_level):
        self.request_id = request_id
        self.total_chunks = None
        self.assistant = assistant
        self.explanation_level = explanation_level
        logger.bind(request_id=self.request_id)


    async def initiate(self, file_path: str):

        vector_store = await create_vector_store()
        logger.info(f"Vector store 생성: {vector_store.id}")

        file_batch = await add_file_to_vector_store(file_path, vector_store)
        logger.info(f"Text file upload 완료: {file_batch.id}")

        thread = await create_thread_with_vector_store(vector_store.id)
        logger.info(f"Thread 생성: {thread.id}")
        return thread, vector_store

    async def create_indices(self, thread):
        logger.info(f"목차 생성 시작 | Thread ID: {thread.id}")
        run = await run_stream(self.assistant.id, thread.id, event_handler=IndexEventHandler(self.request_id))

    async def create_explanations(self, dir_path):
        logger.info("설명문 생성 시작 - 분할된 텍스트 파일들 병렬 처리")

        chunk_files = os.listdir(dir_path)
        self.total_chunks = len(chunk_files)

        tasks = [
            self.create_chunk_explanation(os.path.join(dir_path, chunk_file_name), idx)
            for idx, chunk_file_name in enumerate(chunk_files)
        ]

        results = await asyncio.gather(*tasks)
        logger.info("모든 설명문 생성 작업이 완료되었습니다.")
        return results

    async def create_chunk_explanation(self, chunk_file_path, chunk_index):
        thread, vector_store = await self.initiate(chunk_file_path)
        event_handler = ExplanationEventHandler(
            vector_store=vector_store, request_id=self.request_id, chunk_index=chunk_index
        )

        logger.info(
            f"설명문 생성 시작 | 파일: {chunk_file_path} | Thread ID: {thread.id} | 청크: {chunk_index + 1}/{self.total_chunks}")
        await run_stream(self.assistant.id, thread.id, event_handler=event_handler)

        logger.info(f"설명문 생성 완료 | Thread ID: {thread.id} | 청크: {chunk_index + 1}/{self.total_chunks}")
        return thread, vector_store

    async def create_feedbacks_for_explanations(self, results):
        logger.info("피드백 텍스트 병렬 생성 시작")
        tasks = [self.create_chunk_feedback(thread, vector_store, idx) for idx, (thread, vector_store) in
                 enumerate(results)]

        await asyncio.gather(*tasks)
        logger.info("모든 피드백 생성 작업이 완료되었습니다.")

    async def create_chunk_feedback(self, thread, vector_store, chunk_index):
        feedback_event_handler = FeedbackEventHandler(
            thread_id=thread.id, vector_store=vector_store, request_id=self.request_id, chunk_index=chunk_index
        )

        logger.info(f"피드백 생성 시작 | Thread ID: {thread.id} | 청크: {chunk_index + 1}/{self.total_chunks}")
        await run_stream(self.assistant.id, thread.id, event_handler=feedback_event_handler)

        logger.info(f"피드백 생성 완료 | Thread ID: {thread.id} | 청크: {chunk_index + 1}/{self.total_chunks}")

    async def create_enhanced_explanations(self, results):
        logger.info("피드백 반영 설명문 텍스트 병렬 생성 시작")
        tasks = [self.create_enhanced_chunk_explanation(thread, vector_store, idx) for idx, (thread, vector_store) in
                 enumerate(results)]

        await asyncio.gather(*tasks)
        logger.info("모든 피드백 반영 설명문 생성 작업이 완료되었습니다.")

    async def create_enhanced_chunk_explanation(self, thread, vector_store, chunk_index):
        enhanced_explanation_event_handler = EnhancedExplanationEventHandler(
            thread_id=thread.id, vector_store=vector_store, request_id=self.request_id, chunk_index=chunk_index
        )

        logger.info(f"피드백 반영 설명문 생성 시작 | Thread ID: {thread.id} | 청크: {chunk_index + 1}/{self.total_chunks}")
        await run_stream(self.assistant.id, thread.id, event_handler=enhanced_explanation_event_handler)

        logger.info(f"피드백 반영 설명문 생성 완료 | Thread ID: {thread.id} | 청크: {chunk_index + 1}/{self.total_chunks}")
