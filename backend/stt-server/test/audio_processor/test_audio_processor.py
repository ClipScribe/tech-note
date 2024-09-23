import os
import io
import unittest
from typing import List
from pydub import AudioSegment, silence
from loguru import logger

from app.audio_processor.audio_processor import split_wav_on_silence, apply_overlap, export_chunks_to_bytes
from app.domain.dto.audio_chunk_dto import AudioChunk


# 단위 테스트 클래스
class TestAudioProcessing(unittest.TestCase):

    def setUp(self):
        # 테스트에 사용할 샘플 WAV 파일 로드
        audio_path = "test_audio/uFpNML82bZE_processed.wav"

        with open(audio_path, 'rb') as f:
            self.test_audio_bytes = f.read()  # self.test_audio_bytes로 저장

    def test_split_wav_on_silence(self):
        logger.info("test_split_wav_on_silence 시작")

        # split_wav_on_silence 함수 호출
        chunks = split_wav_on_silence(self.test_audio_bytes,
                                      min_silence_len=500,
                                      silence_thresh=-40,
                                      keep_silence=500)

        # 청크 리스트가 비어 있지 않은지 확인
        self.assertTrue(len(chunks) > 0, "분할된 청크가 없습니다.")

        # 각 청크가 AudioSegment 타입이고 최소 길이를 충족하는지 확인
        for i, chunk in enumerate(chunks):
            self.assertIsInstance(chunk, AudioSegment, f"청크 {i}는 AudioSegment 타입이 아닙니다.")
            self.assertGreaterEqual(len(chunk), 500, f"청크 {i}의 길이가 500ms 미만입니다.")

        logger.info("test_split_wav_on_silence 완료")

    def test_apply_overlap(self):
        logger.info("test_apply_overlap 시작")
        # 먼저 무음을 기준으로 분할
        chunks = split_wav_on_silence(self.test_audio_bytes,
                                      min_silence_len=500,
                                      silence_thresh=-40,
                                      keep_silence=500)
        # 오버랩 적용
        overlapped_chunks = apply_overlap(chunks,
                                          chunk_length_ms=2000,
                                          overlap_ms=500)
        # 예상 청크 수 확인
        self.assertTrue(len(overlapped_chunks) >= len(chunks))
        logger.info("test_apply_overlap 완료")

    def test_export_chunks_to_bytes(self):
        logger.info("test_export_chunks_to_bytes 시작")
        # 먼저 무음을 기준으로 분할
        chunks = split_wav_on_silence(self.test_audio_bytes,
                                      min_silence_len=500,
                                      silence_thresh=-40,
                                      keep_silence=500)
        # 오버랩 적용
        overlapped_chunks = apply_overlap(chunks,
                                          chunk_length_ms=2000,
                                          overlap_ms=500)
        # 바이트로 변환
        chunk_dto_list = export_chunks_to_bytes(overlapped_chunks)

        # 각 청크가 AudioChunk 인스턴스인지 확인
        for chunk_dto in chunk_dto_list:
            self.assertIsInstance(chunk_dto, AudioChunk)
            self.assertIsInstance(chunk_dto.chunk_data, io.BytesIO)
        logger.info("test_export_chunks_to_bytes 완료")

if __name__ == '__main__':
    logger.add("test_log.log", rotation="1 MB")
    unittest.main()