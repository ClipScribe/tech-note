import asyncio
import json
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable
from loguru import logger

# 자막 목록을 가져오는 함수
async def get_transcript_list(video_id):
    """YouTube 동영상의 자막 목록을 반환하는 함수"""
    try:
        # YouTubeTranscriptApi는 동기 함수이므로 asyncio.to_thread로 비동기로 실행
        transcript_list = await asyncio.to_thread(YouTubeTranscriptApi.list_transcripts, video_id)
        captions = [
            {
                'language': transcript.language,
                'is_generated': transcript.is_generated,
                'language_code': transcript.language_code
            }
            for transcript in transcript_list
        ]
        logger.info("Available captions for video {}: {}", video_id, captions)
        return captions

    except TranscriptsDisabled:
        logger.warning("Transcripts are disabled for video {}", video_id)
        return []
    except VideoUnavailable:
        logger.error("Video {} is unavailable", video_id)
        return []
    except Exception as e:
        logger.exception("An unexpected error occurred while fetching captions: {}", e)
        return []

# 자막 다운로드 및 JSON 배열로 저장하는 함수
async def download_transcript(video_id, language_code='en', save_dir='transcripts'):
    """주어진 동영상 ID로 자막을 다운로드하여 JSON 배열 형식으로 저장하는 함수"""
    try:
        # 유효한 video_id 입력 확인
        if not video_id or not isinstance(video_id, str):
            logger.error("Invalid video_id: {}", video_id)
            return None

        # Ensure the save directory exists
        os.makedirs(save_dir, exist_ok=True)

        # YouTubeTranscriptApi는 동기 함수이므로 asyncio.to_thread로 비동기로 실행
        transcript_list = await asyncio.to_thread(YouTubeTranscriptApi.list_transcripts, video_id)
        selected_transcript = None

        # 수동 생성된 자막을 우선 선택, 없으면 자동 생성된 자막 선택
        for transcript in transcript_list:
            if transcript.language_code == language_code:
                selected_transcript = transcript
                if not transcript.is_generated:
                    logger.info("Manual caption found for video ID: {}", video_id)
                    break
                else:
                    logger.info("Automatic caption found for video ID: {}", video_id)

        if not selected_transcript:
            logger.warning("No transcript found for language '{}' in video ID: {}", language_code, video_id)
            return None

        # 자막 다운로드
        logger.info("Starting transcript download for video ID: {}", video_id)
        transcript = await asyncio.to_thread(selected_transcript.fetch)

        # JSON 배열 형식으로 저장
        file_name = f"{video_id}_{language_code}.json"
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)

        logger.info("Transcript successfully saved to {}", file_path)
        return file_path

    except TranscriptsDisabled:
        logger.warning("Transcripts are disabled for video {}", video_id)
        return None
    except VideoUnavailable:
        logger.error("Video {} is unavailable", video_id)
        return None
    except Exception as e:
        logger.exception("An error occurred while downloading the transcript: {}", e)
        return None