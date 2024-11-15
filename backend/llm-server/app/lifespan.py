import asyncio
from loguru import logger
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer
from app.kafka.kafka_config import STT_RESULT_TOPIC, LLM_REQUEST_TOPIC, KAFKA_BOOTSTRAP_SERVERS
from app.kafka.producer.AsyncKafkaProducer import AsyncKafkaProducer
from app.openai_service.assistant_api_utils import create_assistant_model
from app.kafka.consumer.kafka_consumer import *


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting FastAPI application with Kafka consumers and producer.")

    # Kafka 설정 초기화
    stt_result_consumer = AIOKafkaConsumer(
        STT_RESULT_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="stt_result_group"
    )
    request_consumer = AIOKafkaConsumer(
        LLM_REQUEST_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id="request_consumer_group"
    )
    producer = AsyncKafkaProducer()

    # Kafka 및 Assistant 모델 초기화
    await stt_result_consumer.start()
    await request_consumer.start()
    await producer.start()
    assistant = await create_assistant_model()

    processors = {}
    initial_messages = {}

    # Kafka consumer 및 백그라운드 task 시작
    request_consumer_task = asyncio.create_task(consume_initial_requests(request_consumer, initial_messages=initial_messages))
    stt_result_consumer_task = asyncio.create_task(consume_stt_results(stt_result_consumer, processors, assistant.id))

    try:
        yield
    finally:
        # 종료 시 Kafka consumer 및 task 정리
        request_consumer_task.cancel()
        stt_result_consumer_task.cancel()
        await request_consumer.stop()
        await stt_result_consumer.stop()
        await producer.stop()
        try:
            await request_consumer_task
            await stt_result_consumer_task
        except asyncio.CancelledError:
            logger.info("Kafka consumer tasks successfully cancelled.")