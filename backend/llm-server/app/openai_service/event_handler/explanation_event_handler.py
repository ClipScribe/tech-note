import os

import asyncio
from typing import override

from openai import AssistantEventHandler
from loguru import logger

from app.openai_service.assistant_api_utils import add_file_to_vector_store


class ExplanationEventHandler(AssistantEventHandler):
    def __init__(self, request_id, chunk_index):
        super().__init__()
        self.request_id = request_id
        self.chunk_index = chunk_index
        #self.vector_store = vector_store  # 벡터 스토어 참조
        self.generated_explanation = ""  # 생성된 설명문을 저장할 변수

    @override
    def on_text_delta(self, delta, snapshot):
        # 스트리밍된 설명문 데이터를 누적
        self.generated_explanation += delta.value
        #중간 로깅 추가

    @override
    def on_message_done(self, message):
        # 설명문 생성 완료 시 호출
        logger.info(f"chunk_{self.chunk_index}에 대한 설명문 생성 완료")

        # 디렉토리 경로 생성
        explanation_dir = f"capstone_storage/{self.request_id}/explanation"
        os.makedirs(explanation_dir, exist_ok=True)  # 폴더가 없으면 생성

        # 생성된 설명문을 파일로 저장
        explanation_file_path = f"{explanation_dir}/explanation_{self.request_id}_{self.chunk_index}.txt"
        try:
            with open(explanation_file_path, "w") as f:
                f.write(self.generated_explanation)
            logger.info(f"설명문이 {explanation_file_path}에 저장되었습니다.")
        except Exception as e:
            logger.error(f"설명문을 저장하는 데 실패했습니다: {e}")

        # 생성된 설명문 파일을 벡터 스토어에 업로드 (추가 기능, 비활성화 상태)
        # asyncio.run(add_file_to_vector_store(self.vector_store.id, explanation_file_path))
        # logger.info(f"{self.chunk_index}번째 설명문이 벡터 스토어에 업로드되었습니다.")

