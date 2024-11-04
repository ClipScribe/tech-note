from loguru import logger
from datetime import datetime

from app.transcription_service.transcription_service import TranscriptionService
from app.domain.transcription_result import TranscriptionResult


class ConsumerService:
    """
    소비된 메시지를 처리하는 비즈니스 로직을 담당하는 서비스 클래스.
    """

    def __init__(
            self,
            transcription_service: TranscriptionService,
            kafka_producer_service: KafkaProducerService
    ):
        """
        ConsumerService 초기화.

        Args:
            transcription_service (TranscriptionService): 전사 서비스를 담당하는 클래스.
            kafka_producer_service (KafkaProducerService): Kafka에 메시지를 발행하는 클래스.
        """
        self.transcription_service = transcription_service
        self.kafka_producer_service = kafka_producer_service

    async def process_message(self, message: dict):
        """
        소비된 메시지를 처리하고 전사 결과를 Kafka에 발행합니다.

        Args:
            message (dict): 소비된 메시지 내용.
        """
        try:
            request_id = message.get("request_id")

            if not request_id:
                logger.warning(f"Incomplete message received: {message}")
                return

            # 비동기 전사 수행
            transcription_result: TranscriptionResult = await self.transcription_service.transcribe_async(request_id)

            # 전사 결과를 Kafka에 발행
            self.kafka_producer_service.publish(transcription_result.to_dict())
            logger.info(f"Published transcription result for request_id: {request_id}")
        except Exception as e:
            logger.error(f"Error processing message {message}: {e}")
            raise