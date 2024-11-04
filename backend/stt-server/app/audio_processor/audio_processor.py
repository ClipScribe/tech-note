from pydub import AudioSegment, silence
from typing import List
import io


def split_wav_on_silence(file_bytes: bytes,
                         min_silence_len: int = 500,
                         silence_thresh: int = -40,
                         keep_silence: int = 500) -> List[AudioSegment]:
    """
    무음을 기준으로 WAV 파일을 청크로 분할합니다.

    :param file_bytes: 분할할 WAV 파일의 바이트 데이터
    :param min_silence_len: 무음으로 간주할 최소 길이 (밀리초 단위)
    :param silence_thresh: 무음으로 간주할 음량 임계값 (dBFS)
    :param keep_silence: 각 청크의 시작과 끝에 유지할 무음의 길이 (밀리초 단위)
    :return: AudioSegment 객체들의 리스트
    """
    try:
        audio = AudioSegment.from_file(io.BytesIO(file_bytes), format="wav")
    except Exception as e:
        raise ValueError(f"WAV 파일 로드 중 오류 발생: {e}")

    # 무음을 기준으로 청크 분할
    silent_chunks = silence.split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )

    return silent_chunks


def apply_overlap(chunks: List[AudioSegment],
                  chunk_length_ms: int = 2000,
                  overlap_ms: int = 500) -> List[AudioSegment]:
    """
    각 청크에 오버랩을 적용하여 최종 청크 리스트를 생성합니다.

    :param chunks: 무음을 기준으로 분할된 AudioSegment 리스트
    :param chunk_length_ms: 각 청크의 최대 길이 (밀리초 단위)
    :param overlap_ms: 청크 간 오버랩 길이 (밀리초 단위)
    :return: 오버랩이 적용된 AudioSegment 리스트
    """
    final_chunks = []

    for chunk in chunks:
        start_ms = 0
        while start_ms < len(chunk):
            end_ms = start_ms + chunk_length_ms
            sub_chunk = chunk[start_ms:end_ms]
            final_chunks.append(sub_chunk)
            start_ms += (chunk_length_ms - overlap_ms)

    return final_chunks


def export_chunks_to_bytes(chunks: List[AudioSegment]) -> List[bytes]:
    """
    AudioSegment 청크들을 WAV 형식의 바이트 리스트로 변환합니다.

    :param chunks: AudioSegment 청크 리스트
    :return: WAV 형식의 청크 바이트 리스트
    """
    chunk_bytes_list = []
    for chunk in chunks:
        chunk_io = io.BytesIO()
        chunk.export(chunk_io, format="wav")
        chunk_bytes_list.append(chunk_io.getvalue())
    return chunk_bytes_list