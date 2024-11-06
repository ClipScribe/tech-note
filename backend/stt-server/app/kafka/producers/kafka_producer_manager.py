from aiokafka import AIOKafkaProducer
from loguru import logger
import json

from app.domain.kafka_message.chunk_transcription_result import TranscriptionResultMessage
from app.kafka.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    STT_RESULT_TOPIC,
    ACKS,
    MAX_BATCH_SIZE,
    LINGER_MS,
    RETRY_BACKOFF_MS
)


class AsyncSTTResultProducer:
    def __init__(self, topic=STT_RESULT_TOPIC):
        """
        AsyncSTTResultProducer 초기화 시 Kafka 설정을 사용해 프로듀서를 구성.
        - 최신 aiokafka 파라미터에 맞춰 설정.
        """
        self.topic = topic
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks=ACKS,
            max_batch_size=MAX_BATCH_SIZE,
            linger_ms=LINGER_MS,
            retry_backoff_ms=RETRY_BACKOFF_MS
        )

    async def start(self):
        """비동기 프로듀서 시작"""
        await self.producer.start()

    async def stop(self):
        """비동기 프로듀서 종료"""
        await self.producer.stop()

    async def send_stt_result(self, chunk_transcription_result: TranscriptionResultMessage):
        """
        Kafka로 비동기 메시지를 전송.
        """
        try:
            # 메시지 직렬화 전 로깅
            message_data = chunk_transcription_result.model_dump()
            logger.info(f"Serialized JSON message data: {message_data}")

            # 메시지 전송
            await self.producer.send_and_wait(self.topic, value=message_data)
            logger.info(f"Successfully sent message to topic {self.topic}: {chunk_transcription_result}")
        except Exception as e:
            logger.error(f"Failed to send message to topic {self.topic}: {e}")
            # 필요시 재시도 로직 추가







