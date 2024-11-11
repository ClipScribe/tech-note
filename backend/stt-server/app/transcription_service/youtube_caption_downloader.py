import asyncio
import sys

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable
from loguru import logger
import os

# 로그 포맷 설정 (필요에 따라 변경 가능)
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")


# 자막 목록을 가져오는 함수
async def get_transcript_list(video_id):
    """YouTube 동영상의 자막 목록을 반환하는 함수"""
    try:
        # YouTubeTranscriptApi는 동기 함수이므로 asyncio.to_thread로 비동기로 실행
        transcript_list = await asyncio.to_thread(YouTubeTranscriptApi.list_transcripts, video_id)
        captions = []

        for transcript in transcript_list:
            captions.append({
                'language': transcript.language,
                'is_generated': transcript.is_generated,
                'language_code': transcript.language_code
            })
        logger.info("Possible captions: {}", captions)
        return captions

    except TranscriptsDisabled:
        logger.info("Transcripts are disabled for video {}", video_id)
        return []
    except VideoUnavailable:
        logger.info("Video {} is unavailable", video_id)
        return []
    except Exception as e:
        logger.exception("An error occurred: {}", e)
        return []

# 자막 다운로드 및 저장 함수
async def download_transcript(video_id, language_code='en', save_dir='transcripts'):
    """주어진 동영상 ID로 자막을 다운로드하여 텍스트 파일로 저장하는 함수"""
    try:
        # Ensure the save directory exists
        os.makedirs(save_dir, exist_ok=True)

        # YouTubeTranscriptApi는 동기 함수이므로 asyncio.to_thread로 비동기로 실행
        transcript_list = await asyncio.to_thread(YouTubeTranscriptApi.list_transcripts, video_id)
        selected_transcript = None

        # 수동 생성된 자막을 우선 선택
        for transcript in transcript_list:
            if transcript.language_code == language_code and not transcript.is_generated:
                selected_transcript = transcript
                logger.info("Written script exists for video ID: {}", video_id)
                break

        # 자동 생성된 자막을 선택 (수동 자막이 없을 경우)
        if not selected_transcript:
            logger.info("There is no written caption for video ID: {}", video_id)
            for transcript in transcript_list:
                if transcript.language_code == language_code:
                    selected_transcript = transcript
                    logger.info("Generated caption selected for video ID: {}", video_id)
                    break

        if not selected_transcript:
            logger.info("No transcript found for language '{}' in video ID: {}", language_code, video_id)
            return None

        # 자막 다운로드
        logger.info("Starting transcript download for video ID: {}", video_id)
        # Fetch transcript asynchronously
        transcript = await asyncio.to_thread(selected_transcript.fetch)
        transcript_text = '\n'.join([f"{entry['start']} - {entry['text']}" for entry in transcript])

        # 파일 저장
        file_name = f"{video_id}_{language_code}.txt"
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
        logger.info("Transcript saved to {}", file_path)
        return file_path

    except Exception as e:
        logger.exception("An error occurred while downloading the transcript: {}", e)
        return None