from loguru import logger
from app.transcription_service.youtube_caption_downloader import *
from app.domain.kafka_message.chunk_transcription_result import TranscriptionResultMessage

class MessageProcessor:
    def __init__(self, youtube_caption_service, producer):
        self.youtube_caption_service = youtube_caption_service
        self.producer = producer

    def chunk_text(self, text):
        lines = text.splitlines()
        chunks = [
            '\n'.join(lines[i:i + self.chunk_size])
            for i in range(0, len(lines), self.chunk_size)
        ]
        return chunks

    async def process_message(self, message: dict):
        """
        메시지 처리 흐름을 관리하는 메서드

        Args:
            message (dict): Kafka에서 수신한 메시지
        """
        youtube_url = message.get('youtube_url')
        logger.info(f"메시지 처리 시작: {message}")

        #자막 다운로드
        caption_text = download_transcript(youtube_url)

        #자막을 분할
        chunks = self.chunk_text(caption_text)

        #chunk_list를 순회하면서 메시지를 만들고 발행
        chunk_id =0
        for chunk in chunks:
            chunk_message = TranscriptionResultMessage(
            request_id = message.get('request_id'),
            chunk_id = chunk_id,
            transcription_text = chunk,
            )
            chunk_id += 1
            self.producer.send_(chunk_message)