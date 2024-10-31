from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

import logging

logger = logging.getLogger(__name__)

class YoutubeUtils:
    '''
    유튜브 다운로드 처리 관련 클래스
    '''

    @staticmethod
    async def has_manual_subtitles(video_id, language):
        try:
            # 비디오의 자막 리스트를 가져옴
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # 모든 사용 가능한 자막 정보 로깅
            logger.info(f"비디오 {video_id}의 사용 가능한 자막:")
            for transcript in transcript_list:
                subtitle_type = '수동' if not transcript.is_generated else '자동'
                logger.info(f"  - 언어: {transcript.language}, 종류: {subtitle_type}")

            # 수동 자막 확인
            manual_transcript = next((t for t in transcript_list if not t.is_generated and t.language_code == language),
                                     None)
            if manual_transcript:
                logger.info(f"비디오 {video_id}에 수동 {language} 자막이 있습니다.")
                return True

            logger.info(f"비디오 {video_id}에 {language} 자막이 없습니다.")
            return False

        except Exception as e:
            logger.error(f"비디오 {video_id}의 자막 확인 중 오류 발생: {str(e)}")
            return False


