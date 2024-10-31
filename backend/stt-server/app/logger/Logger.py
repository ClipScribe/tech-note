# app/logger/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler
from app.config.settings import Settings

class Logger:
    def __init__(self):
        """
        Logger 초기화 메서드
        """
        settings = Settings()
        log_file = settings.LOG_FILE

        # 로그 디렉토리가 존재하지 않으면 생성
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # 로거 생성
        self.logger = logging.getLogger("KafkaSTTLogger")
        self.logger.setLevel(logging.INFO)

        # 로거가 이미 설정되어 있는지 확인 (중복 핸들러 방지)
        if not self.logger.handlers:
            # 파일 핸들러 설정 (로그 파일에 기록)
            file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
            file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            # 콘솔 핸들러 설정 (콘솔에 출력)
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

    def log_info(self, message: str):
        """
        정보 로그 기록

        Args:
            message (str): 로그 메시지
        """
        self.logger.info(message)

    def log_error(self, message: str):
        """
        오류 로그 기록

        Args:
            message (str): 로그 메시지
        """
        self.logger.error(message)

    def log_warning(self, message: str):
        """
        경고 로그 기록

        Args:
            message (str): 로그 메시지
        """
        self.logger.warning(message)

    def log_debug(self, message: str):
        """
        디버그 로그 기록

        Args:
            message (str): 로그 메시지
        """
        self.logger.debug(message)