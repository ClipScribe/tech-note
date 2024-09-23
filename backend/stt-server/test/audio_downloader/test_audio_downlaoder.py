import unittest

import os
from app.audio_downloader.audio_downloader import AudioDownloader  # AudioDownloader 클래스가 있는 모듈을 임포트합니다.

def test_audio_downloader():
    # 다운로드 디렉토리를 설정합니다.
    download_dir = "test_downloads"
    os.makedirs(download_dir, exist_ok=True)

    # AudioDownloader 인스턴스를 생성합니다.
    downloader = AudioDownloader(download_dir=download_dir)

    # 테스트할 유튜브 동영상 URL을 지정합니다.
    youtube_url = "https://www.youtube.com/watch?v=nXVvvRhiGjI&list=PL590L5WQmH8doPo8OufXavO2Qu4ysZjyl&index=4"  # 예시 URL입니다.

    # 오디오를 다운로드합니다.
    output_path = downloader.download_audio(youtube_url)

    # 다운로드가 성공적으로 이루어졌는지 확인합니다.
    if output_path and os.path.exists(output_path):
        print(f"테스트 성공: 오디오가 {output_path}에 다운로드되었습니다.")
    else:
        print("테스트 실패: 오디오 다운로드에 실패했습니다.")

    # 테스트 후 생성된 파일 및 디렉토리를 정리합니다.
    if output_path and os.path.exists(output_path):
        os.remove(output_path)
    if os.path.exists(download_dir):
        os.rmdir(download_dir)

if __name__ == "__main__":
    test_audio_downloader()
