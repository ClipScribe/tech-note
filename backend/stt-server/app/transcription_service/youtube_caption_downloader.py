from os import cpu_count

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable
import aiohttp
import asyncio

from loguru import logger

# 자막 목록을 가져오는 함수
async def get_transcript_list(video_id):
    """YouTube 동영상의 자막 목록을 반환하는 함수"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        captions = []

        for transcript in transcript_list:
            captions.append({
                'language': transcript.language,
                'is_generated': transcript.is_generated,
                'language_code': transcript.language_code
            })
        logger.info("possible captions : ", captions)
        return captions

    except TranscriptsDisabled:
        logger.info(f'Transcripts are disabled for video {video_id}')
        return []
    except VideoUnavailable:
        logger.info(f'Video {video_id} is unavailable')
        return []
    except Exception as e:
        logger.exception(f'An error occurred: {e}')
        return []


# 자막 다운로드 함수
async def download_transcript(video_id, language_code='en'):
    """주어진 동영상 ID로 수동 생성된 자막을 우선하여 다운로드하는 함수"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        selected_transcript = None

        # 수동 생성된 자막을 우선 선택
        for transcript in transcript_list:
            if transcript.language_code == language_code and not transcript.is_generated:
                selected_transcript = transcript
                logger.info("written script exists for video id: ", video_id)
                break

        # 자동 생성된 자막을 선택 (수동 자막이 없을 경우)
        if not selected_transcript:
            logger.info("there is no written caption for video id: ", video_id)
            for transcript in transcript_list:
                if transcript.language_code == language_code:
                    selected_transcript = transcript
                    logger.info("generated caption selected for video id: ", video_id)
                    break

        if not selected_transcript:
            logger.info(f'No transcript found for language {language_code} in video id: {video_id}')
            return None

        # 자막 다운로드
        logger.info("자막 다운로드 시작 for video id: ", video_id)
        transcript = selected_transcript.fetch()
        transcript_text = '\n'.join([f"{entry['start']} - {entry['text']}" for entry in transcript])
        return transcript_text

    except Exception as e:
        print(f'An error occurred while downloading the transcript: {e}')
        return None