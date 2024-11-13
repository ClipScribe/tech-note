import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import AssistantEventHandler

from app.domain.dto.combined_segment import CombinedSegment
from app.openai_service.assistant_video_explainer_config import name, instructions, model
from loguru import logger

# 환경 변수 로드
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

# Assistant 생성 함수
async def create_assistant_model():
    logger.info("Assistant 모델 생성 중...")
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model
    )
    logger.success("Assistant 모델 생성 완료.")
    return assistant

# 스레드 생성 함수
async def create_thread():
    logger.info("새로운 스레드 생성 중...")
    thread = client.beta.threads.create()
    logger.success(f"스레드 생성 완료: {thread.id}")
    return thread

#vector store 생성 함수
async def create_vector_store():
    logger.info("새로운 vector store 생성 중...")
    vector_store = client.beta.vector_stores.create()
    logger.success(f"vector store 생성 완료: {vector_store.id}")
    return vector_store

# 스레드에 메시지 추가 함수
async def add_message_to_thread(thread_id: str, content: CombinedSegment):
    logger.info(f"스레드 {thread_id}에 메시지 추가 중...")
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content.model_dump_json()
    )
    logger.success("메시지 추가 완료.")
    return message

#vector store에 파일 업로드
async def add_file_to_vector_store(vector_store_id, file_path):
    logger.info("file stream 시작")
    file_stream = open(file_path, 'rb')
    logger.info("file upload 시작")
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_stream
    )
    logger.success("file upload완료")
    return file_batch

# Assistant 스레드 실행 함수
async def run_assistant_thread(assistant_id: str, thread_id: str):
    logger.info(f"Assistant {assistant_id}의 스레드 {thread_id} 실행 중...")
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    logger.success("Assistant 스레드 실행 완료.")
    return run

#생성된 vector store를 사용하는 thread생성
async def create_thread_with_vector_store(vector_store_id: str):
    thread = client.beta.threads.create(
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        }
    )

# 스트리밍 실행 함수
async def run_stream(assistant_id: str, thread_id: str, event_handler: AssistantEventHandler):
    logger.info("스트리밍 시작.")
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions,
        event_handler=event_handler
    ) as stream:
        stream.until_done()
    logger.success("스트리밍 완료.")


# 스레드에서 메시지 목록 가져오기 함수
async def get_response(thread):
    logger.info(f"스레드 {thread.id}의 메시지 목록 가져오는 중...")
    response = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    logger.success("메시지 목록 가져오기 완료.")
    return response

# 스레드 삭제 함수
async def close_thread(thread_id):
    logger.info(f"스레드 {thread_id} 삭제 중...")
    deletion_status = client.beta.threads.delete(thread_id=thread_id)
    logger.success("스레드 삭제 완료.")
    return deletion_status



