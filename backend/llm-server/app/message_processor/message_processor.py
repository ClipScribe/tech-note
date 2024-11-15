import asyncio

from loguru import logger

from app.openai_service.EnhancedExplanationEventHandler import EnhancedExplanationEventHandler
from app.openai_service.ExplanationEventHandler import ExplanationEventHandler
from app.openai_service.FeedbackEventHandler import FeedbackEventHandler
from app.openai_service.IndexEventHandler import IndexEventHandler
from app.openai_service.assistant_api_utils import *

async def initiate(file_path:str):
    vector_store = await create_vector_store()
    logger.info(f"vector store 생성 : {vector_store.id}")

    file_batch = await add_file_to_vector_store(file_path, vector_store)
    logger.info(f"text_file upload : {file_batch.id}")

    thread = await create_thread_with_vector_store(vector_store.id)
    logger.info(f"thread 생성: {thread.id}")
    return thread, vector_store

async def create_indices(thread, assistant, request_id):
    logger.info("목차 생성 시작")
    logger.info(f"run 시작 for thread_id = {thread.id}")
    run = await run_stream(assistant.id, thread.id, event_handler = IndexEventHandler(request_id))

# 설명문 생성 함수 (분할된 텍스트 파일들을 병렬 처리)
async def create_explanations(dir_path, assistant, vector_store):
    logger.info("설명문 생성 시작 - 분할된 텍스트 파일들 병렬 처리")

    tasks = []  # 병렬 처리할 작업 목록
    chunk_files = os.listdir(dir_path)
    total_chunks = len(chunk_files)

    # 분할된 텍스트 파일들이 있는 디렉토리 내의 모든 파일을 반복 처리
    for chunk_index, chunk_file_name in enumerate(chunk_files):
        full_path = os.path.join(dir_path, chunk_file_name)

        # 비동기 태스크 생성
        tasks.append(create_chunk_explanation(full_path, assistant, chunk_index, total_chunks))

        # 모든 태스크를 병렬로 실행하고 각 태스크의 결과를 수집
        results = await asyncio.gather(*tasks)

        # 수집된 결과에서 thread와 vector_store를 추출하여 사용
        for thread, vector_store in results:
            logger.info(f"Thread ID: {thread.id}, Vector Store ID: {vector_store.id}를 피드백 작업에서 사용할 수 있음")

        return results  # 결과를 반환하여 이후의 피드백 처리에 사용할 수 있게 함


# 각 파일에 대해 설명문을 생성하고 벡터 스토어에 업로드하는 비동기 함수
async def create_chunk_explanation(chunk_file_path, assistant, request_id, chunk_index, total_chunks):

    thread, vector_store = initiate(chunk_file_path)

    # ExplanationEventHandler 생성
    event_handler = ExplanationEventHandler(vector_store=vector_store, request_id = request_id ,chunk_index=chunk_index)

    # 설명문 생성 시작
    logger.info(f"{chunk_file_path}에 대한 설명문 생성을 시작합니다.")
    run = await run_stream(assistant.id, thread.id, event_handler=event_handler)

    # 진행 상황 로그
    logger.info(f"{thread.id}-- 설명문 생성 완료 ({chunk_index + 1}/{total_chunks})")
    return thread, vector_store


# 피드백 텍스트를 병렬로 생성하는 함수
async def create_feedbacks_for_explanations(results, assistant, request_id):
    logger.info("피드백 텍스트 병렬 생성 시작")

    # 병렬 처리할 작업 목록
    tasks = []

    # 각 결과에서 thread와 vector_store를 사용하여 피드백 텍스트 생성 작업을 추가
    for chunk_index,thread, vector_store in enumerate(results):
        task = create_chunk_feedback(thread, assistant,vector_store,request_id=request_id,chunk_index = chunk_index)
        tasks.append(task)

    # 모든 피드백 생성 태스크를 병렬로 실행
    await asyncio.gather(*tasks)

async def create_chunk_feedback(thread, assistant, vector_store, request_id, total_chunks, chunk_index):
    logger.info(f"{thread.id}에 대한 피드백 텍스트 생성을 시작합니다.")

    # 피드백 이벤트 핸들러 생성
    feedback_event_handler = FeedbackEventHandler(thread_id=thread.id, vector_store=vector_store, request_id=request_id, chunk_index=chunk_index)

    # 피드백 텍스트 생성 시작
    await run_stream(assistant.id, thread.id, event_handler=feedback_event_handler)
    logger.info(f"{thread.id}-- 설명문 피드백 생성 완료 ({chunk_index + 1})")

# 설명문 생성 함수 (분할된 텍스트 파일들을 병렬 처리)
async def create_enhanced_explanations(results, assistant):
    logger.info("피드백 반영 설명문 텍스트 병렬 생성 시작")

    # 병렬 처리할 작업 목록
    tasks = []

    # 각 결과에서 thread와 vector_store를 사용하여 피드백 텍스트 생성 작업을 추가
    for thread, vector_store in results:
        task = create_enhanced_chunk_explanation(thread, assistant)
        tasks.append(task)

    # 모든 피드백 생성 태스크를 병렬로 실행
    await asyncio.gather(*tasks)


# 각 파일에 대해 설명문을 생성하고 벡터 스토어에 업로드하는 비동기 함수
async def create_enhanced_chunk_explanation(thread, assistant):
    logger.info(f"{thread.id}에 대한 피드백 반영 설명문 텍스트 생성을 시작합니다.")

    # 피드백 이벤트 핸들러 생성
    enhanced_explanation_event_handler = EnhancedExplanationEventHandler(thread_id=thread.id, vector_store=vector_store)

    # 피드백 텍스트 생성 시작
    await run_stream(assistant.id, thread.id, event_handler=enhanced_explanation_event_handler)