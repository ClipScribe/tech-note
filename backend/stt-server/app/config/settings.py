# settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    download_dir: str = "downloads"

    class Config:
        env_file = ".env"  # .env 파일에서 환경 변수 로드
        env_file_encoding = 'utf-8'