import os
import yt_dlp
from typing import Optional
from loguru import logger



class AudioDownloader:
    def __init__(self, download_dir: str = "downloads"):
        """
        VideoDownloader 클래스의 초기화 메서드입니다.

        :param download_dir: 오디오 파일을 다운로드할 디렉토리 경로
        """
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def download_audio(self, youtube_url: str, format: str = 'wav') -> Optional[str]:
        """
        유튜브 URL로부터 오디오를 다운로드하여 지정된 형식으로 저장합니다.

        :param youtube_url: 오디오를 다운로드할 유튜브 동영상의 URL
        :param format: 저장할 오디오 파일 형식 (기본: 'wav')
        :return: 다운로드된 오디오 파일의 경로 또는 None
        """
        unique_filename = youtube_url.split('/')[-1]
        output_path = os.path.join(self.download_dir, unique_filename)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            logger.info(f"Downloaded audio to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return None


