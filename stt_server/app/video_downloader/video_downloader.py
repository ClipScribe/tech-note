import os
import uuid
import yt_dlp
from pydub import AudioSegment
import ffmpeg
from typing import Optional


class VideoDownloader:
    class VideoDownloader:
        def __init__(self, download_dir: str = "downloads"):
            """
            VideoDownloader 클래스의 초기화 메서드입니다.

            :param download_dir: 오디오 파일을 다운로드할 디렉토리 경로
            """
            self.download_dir = download_dir
            os.makedirs(self.download_dir, exist_ok=True)

    def _generate_unique_filename(self, extension: str) -> str:
        """
        고유한 파일 이름을 생성합니다.

        :param extension: 파일 확장자 (예: 'wav')
        :return: 고유한 파일 이름 문자열
        """
        return f"{uuid.uuid4()}.{extension}"

    def download_audio(self, youtube_url: str, format: str = 'wav') -> Optional[str]:
        """
        유튜브 URL로부터 오디오를 다운로드하여 지정된 형식으로 저장합니다.

        :param youtube_url: 오디오를 다운로드할 유튜브 동영상의 URL
        :param format: 저장할 오디오 파일 형식 (기본: 'wav')
        :return: 다운로드된 오디오 파일의 경로 또는 None
        """
        unique_filename = self._generate_unique_filename(format)
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
            print(f"Downloaded audio to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None

    def resample_audio(self, input_path: str, target_sample_rate: int = 16000) -> Optional[str]:
        """
        오디오 파일의 샘플레이트를 변경하여 저장합니다.

        :param input_path: 샘플레이트를 변경할 원본 오디오 파일 경로
        :param target_sample_rate: 목표 샘플레이트 (기본: 16000Hz)
        :return: 샘플레이트가 변경된 오디오 파일의 경로 또는 None
        """
        if not os.path.isfile(input_path):
            print(f"Input file does not exist: {input_path}")
            return None

        try:
            audio = AudioSegment.from_file(input_path)
            resampled_audio = audio.set_frame_rate(target_sample_rate)

            unique_filename = self._generate_unique_filename("wav")
            output_path = os.path.join(self.download_dir, unique_filename)

            resampled_audio.export(output_path, format="wav")
            print(f"Resampled audio saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error resampling audio: {e}")
            return None

    def download_and_resample(self, youtube_url: str, format: str = 'wav', target_sample_rate: int = 16000) -> Optional[str]:
        """
        오디오를 다운로드하고 샘플레이트를 변경하는 전체 과정을 수행합니다.

        :param youtube_url: 오디오를 다운로드할 유튜브 동영상의 URL
        :param format: 저장할 오디오 파일 형식 (기본: 'wav')
        :param target_sample_rate: 목표 샘플레이트 (기본: 16000Hz)
        :return: 샘플레이트가 변경된 오디오 파일의 경로 또는 None
        """
        downloaded_path = self.download_audio(youtube_url, format)
        if not downloaded_path:
            return None

        resampled_path = self.resample_audio(downloaded_path, target_sample_rate)
        if resampled_path:
            # 원본 파일 삭제 (선택 사항)
            try:
                os.remove(downloaded_path)
                print(f"Original file deleted: {downloaded_path}")
            except Exception as e:
                print(f"Error deleting original file: {e}")
        return resampled_path

    def clean_downloads(self):
        """
        다운로드 디렉토리 내의 모든 파일을 삭제합니다.
        """
        try:
            for filename in os.listdir(self.download_dir):
                file_path = os.path.join(self.download_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error cleaning downloads: {e}")
