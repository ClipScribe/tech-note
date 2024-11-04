from app.transcription_service.transcription_service import TranscriptionService
from loguru import logger
from aiokafka import AIOKafkaConsumer
import json
import asyncio


class KafkaApiRequestConsumer:
    def __init__(
        self,
        bootstrap_servers: str,
        consume_topic: str,
        consumer_service: ConsumerService
    ):
        """
        KafkaApiRequestConsumer 초기화.

        Args:
            bootstrap_servers (str): Kafka 브로커 주소.
            consume_topic (str): 소비할 Kafka 토픽 이름.
            consumer_service (ConsumerService): 메시지 처리를 담당하는 서비스 클래스.
        """
        try:
            logger.info(f"Initializing KafkaApiRequestConsumer with servers: {bootstrap_servers}, topic: {consume_topic}.")
            self.consumer = KafkaConsumer(
                consume_topic,
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='transcription-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            self.consume_topic = consume_topic
            self.consumer_service = consumer_service
            logger.info("KafkaApiRequestConsumer initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize KafkaApiRequestConsumer: {e}")
            raise

    async def consume_messages(self):
        """
        Kafka 토픽에서 메시지를 소비하고 ConsumerService를 통해 처리합니다.
        """
        logger.info(f"Starting to consume messages from topic '{self.consume_topic}'.")
        for message in self.consumer:
            try:
                logger.info(f"Received message: {message.value}")
                await self.consumer_service.process_message(message.value)
            except Exception as e:
                logger.error(f"Error processing message {message.value}: {e}")
                continue




