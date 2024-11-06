import io
import numpy as np
from datetime import datetime
from typing import Dict
from loguru import logger
from pydub import AudioSegment
import asyncio

from app.domain.dto.audio_chunk_dto import AudioChunk
from app.domain.dto.transcription_result_dto import TranscriptionResult
from transformers import WhisperForConditionalGeneration, WhisperProcessor


class TranscriptionService:
    def __init__(
            self,
            model_path: str,
            language: str = "en",
            use_gpu: bool = True,
            max_concurrent_tasks: int = 2,
            quantize: bool = False
    ):
        try:
            logger.info(f"Loading Whisper model from '{model_path}' with language '{language}'.")
            self.model = WhisperForConditionalGeneration.from_pretrained(
                model_path, local_files_only=True
            )
            self.processor = WhisperProcessor.from_pretrained(model_path)
            logger.info("Local model loaded successfully.")
        except Exception as e:
            logger.warning(f"Local model not found. Loading temporary model from Hugging Face Hub due to: {e}")
            # 임시 모델로 대체
            self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
            self.processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
            logger.info("Temporary model 'openai/whisper-tiny' loaded.")

        # 모델 설정
        if quantize:
            self.model = self.model.half()
            logger.info("Whisper model을 FP16으로 양자화.")

        self.model = self.model.to("cuda" if use_gpu else "cpu")
        logger.info(f"Whisper model을 {'GPU' if use_gpu else 'CPU'}로 실행.")
        self.language = language
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
        logger.info(f"TranscriptionService initialized with max_concurrent_tasks={max_concurrent_tasks}.")

    async def transcribe_async(self, audio_chunk: AudioChunk) -> TranscriptionResult:
        async with self.semaphore:
            try:
                # AudioSegment로 BytesIO 데이터를 읽어 ndarray로 변환
                audio_segment = AudioSegment.from_file(audio_chunk.chunk_data, format="wav")
                audio_data = np.array(audio_segment.get_array_of_samples()).astype(np.float32) / 32768.0

                # 입력 변환 및 전사 실행
                inputs = self.processor(audio_data, sampling_rate=16000, return_tensors="pt").input_features
                inputs = inputs.to("cuda") if self.model.device == "cuda" else inputs

                # 전사 수행
                generated_ids = self.model.generate(inputs)
                transcription_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

                # 결과 생성
                transcription_result = TranscriptionResult(
                    chunk_id=audio_chunk.chunk_id,
                    transcription_text=transcription_text
                )
                return transcription_result

            except Exception as e:
                logger.error(f"Transcription failed: {e}")
                raise