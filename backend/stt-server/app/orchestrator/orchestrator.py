from loguru import logger
from queue import PriorityQueue

from app.audio_downloader.audio_downloader import AudioDownloader
from app.domain.dto.transcription_result_dto import TranscriptionResult
from app.domain.kafka_message.chunk_transcription_result import TranscriptionResultMessage
from app.kafka.kafka_config import STT_RESULT_TOPIC
from app.kafka.producers.kafka_producer_manager import AsyncProducer
from app.transcription_service.transcription_service import TranscriptionService
from app.audio_processor.audio_processor import *



class Orchestrator:
    def __init__(self, audio_downloader: AudioDownloader, transcription_service: TranscriptionService, kafka_producer: AsyncProducer):
        """
        Orchestrator 초기화 메서드

        Args:
            logger (logger): logger 인스턴스
        """
        self.audio_downloader = audio_downloader
        self.transcription_service = transcription_service
        self.kafka_producer = kafka_producer

    async def transcribe_and_produce(self, request_id: str ,audio_bytes: bytes):
        try:
            # 무음을 기준으로 쪼개기
            silent_chunks = split_wav_on_silence(
                audio_bytes,
                min_silence_len=500,
                silence_thresh=-40,
                keep_silence=500
            )
            #인식률 향상을 위해 오버랩 적용
            overlapped_chunks = apply_overlap(
                silent_chunks,
                chunk_length_ms=2000,
                overlap_ms=500
            )
            #청크로 분할해서 wav 바이트 리스트로 전환
            chunk_dto_list = export_chunks_to_bytes(overlapped_chunks)
            logger.info(f"오디오 청크 분할 완료: 총 {len(chunk_dto_list)} 청크")
        except Exception as e:
            logger.error(f"오디오 청크 분할 실패: {e}")
            return

        # wav chunklist를 순회하면서 STT에 비동기적으로 transcription 요청
        for chunk in chunk_dto_list:
            chunk_transcription = await self.transcription_service.transcribe_async(chunk)

            # Transcript이 완료되면, Kafka 메시지로 생성
            transcription_result_message = TranscriptionResultMessage(
                request_id=request_id,
                chunk_id=chunk_transcription.chunk_id,
                transcription_text=chunk_transcription.transcription_text
            )

            # 생성된 메시지를 logger로 출력하여 확인
            logger.info(f"Generated Kafka message: {transcription_result_message.model_dump()}")

            # Kafka로 발행
            await self.kafka_producer.send_message(transcription_result_message, topic=STT_RESULT_TOPIC)


    async def process_message(self, message: dict):
        """
        메시지 처리 흐름을 관리하는 메서드

        Args:
            message (dict): Kafka에서 수신한 메시지
        """
        youtube_url = message.get('youtube_url')
        logger.info(f"메시지 처리 시작: {message}")
        # 실제 처리 로직은 추후 단계에서 구현됩니다.
        # 2. YouTubeDownloader를 사용하여 wav 다운로드
        audio_path = self.audio_downloader.download_audio(youtube_url)+".wav"
        if not audio_path:
            logger.error("오디오 다운로드에 실패했습니다.")
            return

        # 3. 오디오 파일 읽기
        try:
            with open(audio_path, 'rb') as f:
                audio_bytes = f.read()
            logger.info(f"오디오 파일 읽기 성공: {audio_path}")
        except Exception as e:
            logger.error(f"오디오 파일 읽기 실패: {e}")
            return

        #transcribe하고 produce
        await self.transcribe_and_produce(audio_bytes=audio_bytes, request_id=message.get('request_id'))