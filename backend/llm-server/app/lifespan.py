from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer

from app.kafka.consumer.kafka_consumer import *
from app.kafka.kafka_config import *
from app.kafka.producer.AsyncKafkaProducer import AsyncKafkaProducer
from app.openai_service.assistans_config import *


#나중에 이름, instruction, model 작성해놓은 config 파일 작성하면 됨
@asynccontextmanager
async def lifespan(app):
    logger.info("Starting FastAPI application with Kafka consumers and producer.")

    # Kafka 설정 초기화
    initial_request_consumer = AIOKafkaConsumer(
        LLM_INITIALIZATION_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="llm_initialization_group"
    )
    stt_result_consumer = AIOKafkaConsumer(
        STT_RESULT_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="stt_result_group"
    )
    producer = AsyncKafkaProducer(KAFKA_BOOTSTRAP_SERVERS)

    # Kafka 및 Assistant 모델 초기화
    await stt_result_consumer.start()
    await initial_request_consumer.start()
    await producer.start()
    beginner_assistant = await create_assistant_model(name=BEGINNER_ASSISTANT_NAME,instructions=BEGINNER_INSTRUCTION, model=MODEL)
    intermediate_assistant = await create_assistant_model(name=INTERMEDIATE_ASSISTANT_NAME,instructions=INTERMEDIATE_INSTRUCTION, model=MODEL)
    expert_assistant = await create_assistant_model(name=EXPERT_ASSISTANT_NAME, instructions=EXPER_INSTRUCTION, model=MODEL)

    assistants = {'beginner': beginner_assistant, 'intermediate': intermediate_assistant, 'expert': expert_assistant}


    processors = {}
    initial_messages = {}

    # Kafka consumer 및 백그라운드 task 시작
    request_consumer_task = asyncio.create_task(consume_initial_requests(initial_request_consumer, initial_messages=initial_messages, assistants=assistants, processors=processors))
    stt_result_consumer_task = asyncio.create_task(consume_stt_results(stt_result_consumer, initial_messages=initial_messages, processors=processors))

    try:
        yield
    finally:
        # 종료 시 Kafka consumer 및 task 정리
        request_consumer_task.cancel()
        stt_result_consumer_task.cancel()
        await initial_request_consumer.stop()
        await stt_result_consumer.stop()
        await producer.stop()
        try:
            await request_consumer_task
            await stt_result_consumer_task
        except asyncio.CancelledError:
            logger.info("Kafka consumer tasks successfully cancelled.")

"""
import asyncio
from loguru import logger
from collections import defaultdict
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer
from app.domain.kafka_message.initiate_request_message import InitiateRequestMessage
from app.domain.kafka_message.stt_chunk_result_message import STTChunkResultMessage
from app.message_processor.message_processor import MessageProcessor
from app.text_utils.text_utils import TextMergerToFile
from app.kafka.consumer.kafka_consumer import *
from app.kafka.kafka_config import *
from app.kafka.producer.AsyncKafkaProducer import AsyncKafkaProducer
from app.openai_service.assistants_config import *


async def consume_initial_requests(consumer,producer ,initial_messages, assistants, processors, stt_retry_queue):
    """
    초기 메시지를 소비하여 request_id별 정보를 저장.
    요청이 완료되면 해당 request_id의 정보를 삭제하고, 필요 시 STT 메시지를 재시도 큐에서 가져와 처리합니다.
    """
    logger.info("초기 메시지를 소비하기 시작합니다.")
    try:
        async for msg in consumer:
            logger.info(f"Initial message consume: {msg.value}")
            initial_message = InitiateRequestMessage.model_validate_json(msg.value)

            request_id = initial_message.request_id
            initial_messages[request_id] = initial_message
            logger.info(f"Request ID '{request_id}'의 초기 메시지를 저장했습니다.")

            # 초기 텍스트 파일 생성
            TextMergerToFile.initialize_file(request_id)

            # Processor 생성
            level = initial_message.explanation_level
            processors[request_id] = MessageProcessor(
                request_id=request_id,
                assistant=assistants[level],
                explanation_level=level,
                producer=producer,
            )

            # 재시도 큐에 STT 메시지가 있다면 해당 request_id의 STT 메시지 처리
            if stt_retry_queue[request_id]:
                logger.info(f"재시도 큐에 있는 STT 메시지 처리 시작 for Request ID '{request_id}'")
                for stt_msg in stt_retry_queue.pop(request_id):
                    await process_stt_result(stt_msg, initial_messages, processors)

    except Exception as e:
        logger.error(f"초기 메시지 소비 중 오류 발생: {e}")
    finally:
        logger.info("초기 메시지 소비 종료.")


async def consume_stt_results(consumer, initial_messages, processors, stt_retry_queue):
    """
    STT 결과물을 소비하고 초기 메시지가 준비되지 않은 경우 재시도 큐에 저장합니다.
    """
    logger.info("STT 결과물을 소비하기 시작합니다.")
    try:
        async for msg in consumer:
            logger.info(f"chunk message consume: {msg.value}")
            stt_result = STTChunkResultMessage.model_validate_json(msg.value)

            request_id = stt_result.request_id
            if request_id not in initial_messages:
                # 초기 메시지 미도착: 재시도 큐에 STT 메시지 추가
                stt_retry_queue[request_id].append(stt_result)
                logger.warning(f"Request ID '{request_id}'의 초기 메시지가 준비되지 않았습니다. 재시도 큐에 추가합니다.")
            else:
                # 초기 메시지가 도착한 경우 즉시 처리
                await process_stt_result(stt_result, initial_messages, processors)
    except Exception as e:
        logger.error(f"STT 결과물 소비 중 오류 발생: {e}")
    finally:
        logger.info("STT 결과물 소비 종료.")


async def process_stt_result(stt_result, initial_messages, processors):
    """
    개별 STT 결과 메시지를 처리하고 필요한 작업 수행.
    """
    try:
        request_id = stt_result.request_id
        chunk_id = stt_result.chunk_id
        transcription_text = stt_result.transcription_text

        if request_id in processors:
            message_processor = processors[request_id]
            TextMergerToFile.add_message(request_id, {"request_id": request_id, "chunk_id": chunk_id,
                                                      "transcription_text": transcription_text})
            logger.debug(f"Request ID '{request_id}', Chunk ID '{chunk_id}' 병합 처리 완료.")

            # 모든 청크가 처리되었는지 확인
            total_chunks = initial_messages[request_id].total_chunk_num
            if chunk_id == total_chunks - 1:
                logger.info(f"Request ID '{request_id}'의 모든 청크 병합이 완료되었습니다.")
                transcript_file_path = TextMergerToFile.get_merged_text(request_id)

                # initiate
                initial_thread, initial_vector_store = await message_processor.initiate(transcript_file_path)
                await message_processor.create_indices(initial_thread)

                # 목차에 따라 텍스트 분할
                index_text_path = f"capstone_storage/{request_id}/index/index.txt"
                transcription_chunks_path = TextMergerToFile.split_by_toc(request_id=request_id, toc_filepath=index_text_path)

                # 설명문 생성 및 피드백 처리
                chunk_resource_list = await message_processor.create_explanations(transcription_chunks_path)
                await message_processor.create_feedbacks_for_explanations(chunk_resource_list)
                await message_processor.create_enhanced_explanations(chunk_resource_list)
        else:
            logger.error(f"Request ID '{request_id}'에 대한 Processor가 존재하지 않습니다.")
    except Exception as e:
        logger.error(f"STT 청크 처리 중 오류 발생: {e}")


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting FastAPI application with Kafka consumers and producer.")
    initial_request_consumer, stt_result_consumer, producer, assistants = await initialize_kafka_and_assistants()

    processors = {}
    initial_messages = {}
    stt_retry_queue = defaultdict(list)

    request_consumer_task = asyncio.create_task(
        consume_initial_requests(
            initial_request_consumer, producer ,initial_messages, assistants, processors, stt_retry_queue
        )
    )
    stt_result_consumer_task = asyncio.create_task(
        consume_stt_results(
            stt_result_consumer, initial_messages, processors, stt_retry_queue
        )
    )

    try:
        yield
    finally:
        # 종료 시 정리
        request_consumer_task.cancel()
        stt_result_consumer_task.cancel()
        await initial_request_consumer.stop()
        await stt_result_consumer.stop()
        await producer.stop()
        try:
            await request_consumer_task
            await stt_result_consumer_task
        except asyncio.CancelledError:
            logger.info("Kafka consumer tasks successfully cancelled.")


async def initialize_kafka_and_assistants():
    """
    Kafka 및 Assistant 모델을 초기화하는 함수.
    """
    initial_request_consumer = AIOKafkaConsumer(
        LLM_INITIALIZATION_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="llm_initialization_group"
    )
    stt_result_consumer = AIOKafkaConsumer(
        STT_RESULT_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="stt_result_group"
    )
    producer = AsyncKafkaProducer(KAFKA_BOOTSTRAP_SERVERS)

    # Kafka와 모델 초기화
    await stt_result_consumer.start()
    await initial_request_consumer.start()
    await producer.start()

    beginner_assistant = await create_assistant_model(name=BEGINNER_ASSISTANT_NAME, instructions=BEGINNER_INSTRUCTION, model=MODEL)
    intermediate_assistant = await create_assistant_model(name=INTERMEDIATE_ASSISTANT_NAME, instructions=INTERMEDIATE_INSTRUCTION, model=MODEL)
    expert_assistant = await create_assistant_model(name=EXPERT_ASSISTANT_NAME, instructions=EXPER_INSTRUCTION, model=MODEL)

    assistants = {'beginner': beginner_assistant, 'intermediate': intermediate_assistant, 'expert': expert_assistant}
    return initial_request_consumer, stt_result_consumer, producer, assistants

