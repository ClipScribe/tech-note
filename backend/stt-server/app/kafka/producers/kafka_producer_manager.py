# kafka_producer_manager.py

from aiokafka import AIOKafkaProducer
import json


class STTResultProducer:
    def __init__(self):
        """
        STT 결과를 카프카에 전송하는 프로듀서 클래스.
        - 배치 크기와 대기 시간을 조정하여 배치 처리 최적화.
        - JSON 직렬화 방식 사용.
        - 최소 한 번 전송 보장을 위해 acks=all 설정.
        """
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8'),  # request_id를 메시지 키로 설정
            acks='all',  # 전송 보장 수준 설정
            retries=3,  # 전송 실패 시 최대 3회 재시도
            batch_size=16384,  # 16KB 배치 크기
            linger_ms=20  # 20ms 대기 시간
        )

    def send_stt_result(self, request_id, chunk_id, timestamp, text_chunk):
        """
        Kafka로 STT 결과 메시지를 전송.
        - request_id를 키로 사용하여 동일 파일의 모든 청크가 같은 파티션에 들어가 순서를 보장.
        - 메시지 형식은 JSON으로 직렬화하여 전송.
        """
        message = {
            "request_id": request_id,
            "chunk_id": chunk_id,
            "timestamp": timestamp,
            "text_chunk": text_chunk
        }

        # request_id를 메시지 키로 설정해 같은 파티션에 할당
        self.producer.send(STT_RESULT_TOPIC, key=request_id, value=message)
        self.producer.flush()  # 전송 보장

    def close(self):
        """프로듀서를 안전하게 종료"""
        self.producer.close()