# app/main.py

import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

from app.kafka.consumers.kafka_consumer import consume
from app.kafka.producers import kafka_producer_manager

# 환경 변수 로드
load_dotenv()

async def lifespan(app: FastAPI):
    # 로깅 초기화 (이미 loguru로 설정되었으므로 별도의 설정은 필요 없음)
    logger.info("Starting FastAPI application with Kafka consumer.")

    # 백그라운드 태스크로 Kafka 소비 시작
    consumer_task = asyncio.create_task(consume())

    try:
        yield
    finally:
        # 애플리케이션 종료 시 Kafka 소비자 중지
        logger.info("Shutting down FastAPI application. Cancelling Kafka consumer task.")
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            logger.info("Kafka consumer task cancelled successfully.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "STT Server is running."}