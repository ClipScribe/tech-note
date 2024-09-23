from youtube_transcript_api import YouTubeTranscriptApi
from loguru import logger

class CaptionService:

    @staticmethod
    async def has_manual_subtitles(video_id, language: str = "en")-> bool:
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

    @staticmethod
    def split_subtitles_into_chunks(transcript, chunk_duration=60):
        """
        자막을 chunk_duration 길이로 나누는 메서드.
        - transcript: 전체 자막 리스트
        - chunk_duration: 각 청크의 최대 지속 시간(초 단위)
        """
        chunks = []
        chunk = []
        current_duration = 0
        for subtitle in transcript:
            start_time = subtitle["start"]
            duration = subtitle["duration"]
            text = subtitle["text"]

            if current_duration + duration > chunk_duration:
                chunks.append(chunk)
                chunk = []
                current_duration = 0

            chunk.append({"start": start_time, "duration": duration, "text": text})
            current_duration += duration

        # 마지막 청크 추가
        if chunk:
            chunks.append(chunk)

        return chunks


