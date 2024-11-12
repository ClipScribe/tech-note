import asyncio
from asyncio import get_running_loop
from typing import override
from loguru import logger

from openai import AssistantEventHandler

# EventHandler 클래스 정의
class EventHandler(AssistantEventHandler):
    def __init__(self, request_id, producer, segment_start_time):
        super().__init__()
        self.request_id = request_id
        self.segment_start_time = segment_start_time
        self.producer = producer
        self.buffer = []

    @override
    def on_text_created(self, text) -> None:
        logger.info("스트리밍 응답 생성 시작.")
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        self.buffer.append(delta.value)
        if len(self.buffer) >= 20:
            content = ''.join(self.buffer)
            self.buffer = []  # 버퍼 초기화
            logger.info(f"스트리밍 배치 생성 완료 [{self.request_id}]: {content}")
            asyncio.ensure_future(self.producer.send_llm_content(content))

    @override
    def on_text_done(self, text):
        if self.buffer:
            content = ''.join(self.buffer)
            self.buffer = []  # 버퍼 초기화
            logger.info(f"스트리밍 배치 생성 완료 [{self.request_id}]: {content}")
            asyncio.ensure_future(self.producer.send_llm_content(content))
            asyncio.ensure_future(self.producer.send_content_completed_message())





