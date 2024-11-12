
import asyncio
import aiofiles
import re
from loguru import logger

from app.domain.kafka_message.initialize_llm_request_message import InitiateRequestMessage
from app.kafka.kafka_config import STT_RESULT_TOPIC, LLM_INITIALIZATION_TOPIC
from app.transcription_service.youtube_caption_downloader import *
from app.domain.kafka_message.chunk_transcription_result import TranscriptionResultMessage

class MessageProcessor:
    YOUTUBE_VIDEO_ID_REGEX = re.compile(
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    )

    def __init__(self, producer, chunk_size=7):
        """
        MessageProcessor 클래스 초기화

        :param producer: Kafka 프로듀서 인스턴스
        :param chunk_size: 자막을 분할할 라인 수 (기본값: 7)
        """
        self.producer = producer
        self.chunk_size = chunk_size

    def extract_video_id(self, youtube_url: str) -> str:
        """
        YouTube URL에서 Video ID를 추출하는 메서드

        :param youtube_url: YouTube 동영상 URL
        :return: 추출된 Video ID
        :raises ValueError: Video ID를 추출할 수 없을 경우
        """
        match = self.YOUTUBE_VIDEO_ID_REGEX.search(youtube_url)
        if match:
            return match.group(1)
        else:
            logger.error("Invalid YouTube URL: {}", youtube_url)
            raise ValueError(f"Invalid YouTube URL: {youtube_url}")

    def chunk_text(self, text: str) -> list:
        """
        자막 텍스트를 지정된 라인 수 단위로 묶는 메서드

        :param text: 전체 자막 텍스트
        :return: 일정 단위로 묶인 자막 리스트
        """
        lines = text.splitlines()
        chunks = []
        current_chunk = []
        current_duration = 0.0

        for line in lines:
            current_chunk.append(line)
            if len(current_chunk) >= self.chunk_size:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []

        # 남은 라인이 있을 경우 마지막 청크에 추가
        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        logger.info("Text split into {} chunks", len(chunks))
        return chunks

    async def process_message(self, message: dict):
        """
        메시지 처리 흐름을 관리하는 메서드

        Args:
            message (dict): Kafka에서 수신한 메시지
        """
        youtube_url = message.get('youtube_url')
        request_id = message.get('request_id')
        explanation_level = message.get('explanation_level')

        logger.info("Processing message: {}", message)

        if not youtube_url:
            logger.error("No 'youtube_url' found in message: {}", message)
            return

        try:
            # YouTube URL에서 Video ID 추출
            video_id = self.extract_video_id(youtube_url)
            logger.info("Extracted Video ID: {}", video_id)

            # 자막 다운로드
            caption_file_path = await download_transcript(video_id, language_code='en')
            if not caption_file_path:
                logger.error("Failed to download transcript for Video ID: {}", video_id)
                return

            # 자막 파일 읽기 (비동기적으로 읽기)
            async with aiofiles.open(caption_file_path, 'r', encoding='utf-8') as f:
                caption_text = await f.read()

            if not caption_text:
                logger.error("Downloaded transcript is empty for Video ID: {}", video_id)
                return

            # 자막을 분할
            chunks = self.chunk_text(caption_text)
            total_chunks = len(chunks)
            initial_message = InitiateRequestMessage(
                request_id=request_id,
                total_chunk_num=total_chunks,
                explanation_level = explanation_level,
            )
            await self.producer.send_message(initial_message, topic = LLM_INITIALIZATION_TOPIC)
            logger.info("sent initialization message for request id: {}", request_id)

            initial_message = InitiateRequestMessage(
                request_id=request_id,
                total_chunk_num=total_chunks,
                explanation_level = explanation_level,
            )
            await self.producer.send_message(initial_message, topic = LLM_INITIALIZATION_TOPIC)
            logger.info("sent initialization message for request id: {}", request_id)


            # chunk_list를 순회하면서 메시지를 만들고 발행
            for chunk_id, chunk in enumerate(chunks):
                chunk_message = TranscriptionResultMessage(
                    request_id=request_id,
                    chunk_id=chunk_id,
                    transcription_text=chunk,
                )
                await self.producer.send_message(chunk_message, topic=STT_RESULT_TOPIC)
                logger.info("Sent chunk {} for Video ID: {}", chunk_id, video_id)

            logger.info("Completed processing for Video ID: {}", video_id)

        except ValueError as ve:
            logger.error("ValueError: {}", ve)
        except Exception as e:
            logger.exception("An unexpected error occurred while processing the message: {}", e)
