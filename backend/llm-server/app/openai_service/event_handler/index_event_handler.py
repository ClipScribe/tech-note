import asyncio
import json
import os
from typing import override

from openai import AssistantEventHandler
from loguru import logger
from openai.types.beta.threads import Text

from app.domain.kafka_message.llm_index_message import IndexMessage
from app.kafka.kafka_config import LLM_INDEX_EVENTS
from app.text_utils.text_utils import TextMergerToFile


class IndexEventHandler(AssistantEventHandler):
    def __init__(self, request_id, producer):
        super().__init__()
        self.request_id = request_id
        self.producer = producer
        self.kafka_topic = LLM_INDEX_EVENTS
        self.index_data = ""  # 생성된 목차 데이터를 저장할 변수

    @override
    def on_text_created(self, text: Text) -> None:
        logger.info("목차 생성 시작")

    @override
    def on_text_delta(self, delta, snapshot):
        # 스트리밍된 목차 항목 데이터를 누적
        self.index_data += delta.value

    @override
    def on_message_done(self, message):
        # 전체 목차 생성이 완료된 시점에서 호출
        logger.info("목차 생성 완료")
        logger.info(self.index_data)
        # 디렉터리가 존재하지 않을 경우 생성
        index_dir = f"capstone_storage/{self.request_id}/index"
        os.makedirs(index_dir, exist_ok=True)

        # 생성된 목차와 타임스탬프 정보를 파일로 저장
        index_file_path = f"{index_dir}/index.txt"
        try:
            with open(index_file_path, "w", encoding="utf-8") as f:
                f.write(self.index_data)
                f.flush()  # 디스크에 즉시 쓰기
            logger.info(f"목차 데이터가 {index_file_path}에 저장되었습니다.")
        except Exception as e:
            logger.error(f"목차 파일을 저장하는 중 오류 발생: {e}")

        index_message = IndexMessage(
            videoId = self.request_id,
            indices = self.index_data,
        )

        # 메시지를 JSON으로 직렬화하여 Kafka에 전송
        try:
            asyncio.create_task(
                self.producer.send_message(self.kafka_topic,index_message)
            )
            logger.info(f"Kafka에 메시지가 전송되었습니다 request_id: {self.request_id}")
        except Exception as e:
            logger.error(f"Kafka에 메시지를 전송하는 중 오류가 발생했습니다: {e}")

