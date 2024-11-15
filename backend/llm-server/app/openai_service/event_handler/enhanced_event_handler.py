import os

import asyncio
from typing import override, Text

from loguru import logger
from aiokafka import AIOKafkaProducer
from openai import AssistantEventHandler

from app.domain.kafka_message.llm_result_message import LLMResultMessage


#정의한 메시지로 메시지 교체하고 로깅 추가
class EnhancedExplanationEventHandler(AssistantEventHandler):
    def __init__(self, thread_id, request_id ,chunk_index=None, kafka_producer=None,
                 kafka_topic="explanation_stream"):
        super().__init__()
        self.thread_id = thread_id
        self.request_id = request_id
        self.chunk_index = chunk_index
        self.enhanced_explanation_data = ""
        self.kafka_producer = kafka_producer
        self.kafka_topic = kafka_topic

    @override
    def on_text_created(self, text: Text):
        start_message = f"Explanation generation started for chunk {self.chunk_index}."
        asyncio.run(self.kafka_producer.send_and_wait(self.kafka_topic, value=start_message.encode('utf-8')))

    @override
    def on_text_delta(self, delta, snapshot):
        self.enhanced_explanation_data += delta.value
        #asyncio.run(self.kafka_producer.send_and_wait(self.kafka_topic, value=delta.value.encode('utf-8')))

    @override
    def on_message_done(self, message):
        # 설명문 생성 완료 시 호출
        logger.info(f"chunk_{self.chunk_index}에 대한 설명문 생성 완료")
        # 디렉토리 경로 생성
        explanation_dir = f"capstone_storage/{self.request_id}/enhanced_explanation"
        os.makedirs(explanation_dir, exist_ok=True)  # 폴더가 없으면 생성
        # 생성된 설명문을 파일로 저장
        explanation_file_path = f"{explanation_dir}/enhanced_explanation_{self.request_id}_{self.chunk_index}.txt"
        try:
            with open(explanation_file_path, "w") as f:
                f.write(self.enhanced_explanation_data)
            logger.info(f"설명문이 {explanation_file_path}에 저장되었습니다.")
        except Exception as e:
            logger.error(f"설명문을 저장하는 데 실패했습니다: {e}")
        complete_message = f"Explanation generation completed for chunk {self.chunk_index}."
        asyncio.run(self.kafka_producer.send_and_wait(self.kafka_topic, value=complete_message.encode('utf-8')))

        # LLMResultMessage 형식의 메시지 생성
        complete_message = LLMResultMessage(
            request_id=self.request_id,
            index_id=self.chunk_index,
            content=self.enhanced_explanation_data
        )

        # 메시지를 JSON으로 직렬화하여 Kafka에 전송
        try:
            asyncio.create_task(
                self.kafka_producer.send_and_wait(self.kafka_topic, value=complete_message.model_dump_json().encode('utf-8')))
            logger.info(f"Kafka에 메시지가 전송되었습니다: chunk_{self.chunk_index}")
        except Exception as e:
            logger.error(f"Kafka에 메시지를 전송하는 중 오류가 발생했습니다: {e}")
