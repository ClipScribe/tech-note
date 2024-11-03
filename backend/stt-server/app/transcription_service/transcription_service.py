import io
from datetime import datetime
from typing import Dict
from loguru import logger
import whisper
from pydub import AudioSegment
import asyncio

from app.domain.transcription_result import TranscriptionResult


class TranscriptionService:
    """
    Whisper 모델을 사용하여 오디오 청크를 전사하는 서비스.

    Attributes:
        model (whisper.Model): 로드된 Whisper 모델.
        semaphore (asyncio.Semaphore): 동시 실행 가능한 전사 작업의 수를 제한.
    """

    def __init__(
            self,
            model_name: str = "base",
            language: str = "en",
            use_gpu: bool = True,
            max_concurrent_tasks: int = 2,
            quantize: bool = False
    ):
        """
        TranscriptionService 초기화.

        Args:
            model_name (str): 사용할 Whisper 모델 이름.
            language (str): 전사할 언어.
            use_gpu (bool): GPU 사용 여부.
            max_concurrent_tasks (int): 동시 실행 가능한 전사 작업의 최대 수.
            quantize (bool): 모델 양자화 사용 여부.
        """
        try:
            logger.info(f"Loading Whisper model '{model_name}' with language '{language}'.")
            self.model = whisper.load_model(model_name)

            if quantize:
                # Whisper 모델의 양자화 기능을 지원하는지 확인 후 적용
                # 예시로 모델을 FP16으로 변환
                self.model = self.model.half()
                logger.info("Whisper model을 FP16으로 양자화.")

            if use_gpu:
                self.model = self.model.to("cuda")
                logger.info("Whisper model을 GPU로 실행.")
            else:
                logger.info("Whisper model을 CPU로 실행.")
            self.language = language
            self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
            logger.info(f"TranscriptionService initialized with max_concurrent_tasks={max_concurrent_tasks}.")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    async def transcribe_async(self, audio_chunk: bytes, request_id: str, chunk_id: int) -> TranscriptionResult:
        """
        비동기적으로 오디오 청크를 전사하여 TranscriptionResult 반환.

        Args:
            audio_chunk (bytes): WAV 형식의 오디오 청크 데이터.
            request_id (str): 전사 요청 ID.

        Returns:
            TranscriptionResult: 전사된 텍스트와 메타데이터.
        """
        async with self.semaphore:
            try:
                logger.debug(f"Starting asynchronous transcription for request_id: {request_id}")

                # 오디오 청크를 AudioSegment로 변환
                audio = AudioSegment.from_file(io.BytesIO(audio_chunk), format="wav")
                logger.debug(f"Audio segment duration: {len(audio)}ms")

                # Whisper 모델을 사용하여 전사 수행
                # Whisper의 transcribe 메서드는 파일-like 객체를 받을 수 있다.
                result = self.model.transcribe(io.BytesIO(audio_chunk), language=self.language)
                text = result.get('text', '').strip()
                logger.debug(f"Transcription completed for request_id-chunk_id: {request_id} - {chunk_id}")

                transcription_result = TranscriptionResult(
                    request_id=request_id,
                    chunk_id=chunk_id,
                    text=text,
                    timestamp=datetime.utcnow()
                )
                logger.info(f"Transcription completed for request_id: {transcription_result.request_id}")
                return transcription_result
            except Exception as e:
                logger.error(f"Transcription failed for request_id-chunk_id: {request_id}-{chunk_id}: {e}")
                raise