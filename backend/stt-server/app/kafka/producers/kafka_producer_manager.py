from aiokafka import AIOKafkaProducer
import json

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
            loop=None,  # FastAPI의 이벤트 루프 사용
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8'),
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

    async def send_stt_result(self, request_id, chunk_id, timestamp, text_chunk):
        """
        Kafka로 비동기 메시지를 전송.
        - request_id를 메시지 키로 설정하여 동일 파일의 모든 청크가 같은 파티션으로 들어가도록 함.
        """
        message = {
            "request_id": request_id,
            "chunk_id": chunk_id,
            "timestamp": timestamp,
            "text_chunk": text_chunk
        }

        # 비동기 메시지 전송
        await self.producer.send_and_wait(self.topic, key=request_id, value=message)