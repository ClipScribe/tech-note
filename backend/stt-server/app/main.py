# app/main.py
import uvicorn
import asyncio
import json

from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger
from aiokafka import AIOKafkaConsumer

from app.kafka.kafka_config import *

from app.kafka.consumers.kafka_consumer import consume, consume_request
from app.kafka.producers import kafka_producer_manager
from app.kafka.producers.kafka_producer_manager import AsyncProducer
from app.orchestrator.message_processor import MessageProcessor

# 환경 변수 로드
load_dotenv()

async def lifespan(app: FastAPI):
    logger.info("서버를 시작합니다.")
    consumer = AIOKafkaConsumer(
        VIDEO_REQUEST_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='transcription-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    producer = AsyncProducer()


    logger.info("consumer, producer start")
    await consumer.start()
    await producer.start()

    message_processor = MessageProcessor(producer)

    request_consumer_task = asyncio.create_task(consume_request(consumer,message_processor))

    try:
        yield
    finally:
        # 애플리케이션 종료 시 Kafka 소비자 중지
        logger.info("Shutting down FastAPI application. Cancelling Kafka consumer task.")
        request_consumer_task.cancel()
        await producer.stop()
        await consumer.stop()
        try:
            await request_consumer_task
        except asyncio.CancelledError:
            logger.info("Kafka consumer task cancelled successfully.")

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

@app.get("/")
def read_root():
    return {"message": "STT Server is running."}