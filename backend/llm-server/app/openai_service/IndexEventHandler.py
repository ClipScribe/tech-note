from openai import AssistantEventHandler
from loguru import logger

class IndexEventHandler(AssistantEventHandler):
    def __init__(self, request_id):
        super().__init__()
        self.request_id = request_id
        self.index_data = ""  # 생성된 목차 데이터를 저장할 변수

    async def on_text_delta(self, delta, snapshot):
        # 스트리밍된 목차 항목 데이터를 누적
        self.index_data += delta.value

    async def on_message_done(self, message):
        # 전체 목차 생성이 완료된 시점에서 호출
        logger.info("목차 생성 완료")

        # 생성된 목차와 타임스탬프 정보를 파일로 저장
        with open(f"capstone_storage/{self.request_id}/index/index.txt", "w") as f:
            f.write(self.index_data)
        logger.info("목차 데이터가 generated_index.txt에 저장되었습니다.")