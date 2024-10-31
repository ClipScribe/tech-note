# settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    whisper_model_name: str = "base"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_client_id: str = "whisper-processor"
    kafka_topic: str = "transcripts"
    download_dir: str = "downloads"

    class Config:
        env_file = ".env"  # .env 파일에서 환경 변수 로드
        env_file_encoding = 'utf-8'