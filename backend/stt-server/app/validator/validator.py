# app/validator/validator.py

import re
from urllib.parse import urlparse
from app.logger import Logger

class Validator:
    def __init__(self, logger: Logger):
        """
        Validator 초기화 메서드

        Args:
            logger (Logger): Logger 인스턴스
        """
        self.logger = logger
        # request_id의 유효성을 검증하기 위한 정규 표현식 (예: UUID 형식)
        self.request_id_pattern = re.compile(
            r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[4][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
        )

    def validate_request_id(self, request_id: str) -> bool:
        """
        request_id의 유효성을 검증

        Args:
            request_id (str): 검증할 request_id

        Returns:
            bool: 유효하면 True, 그렇지 않으면 False
        """
        if self.request_id_pattern.match(request_id):
            self.logger.log_info(f"유효한 request_id: {request_id}")
            return True
        else:
            self.logger.log_error(f"유효하지 않은 request_id: {request_id}")
            return False

    def validate_youtube_url(self, url: str) -> bool:
        """
        유튜브 URL의 유효성을 검증

        Args:
            url (str): 검증할 유튜브 URL

        Returns:
            bool: 유효하면 True, 그렇지 않으면 False
        """
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            self.logger.log_error(f"잘못된 URL 스킴: {url}")
            return False
        if parsed_url.netloc not in ('www.youtube.com', 'youtube.com', 'youtu.be'):
            self.logger.log_error(f"유효하지 않은 유튜브 도메인: {url}")
            return False
        # 추가적인 유효성 검증 로직을 여기에 추가할 수 있습니다.
        self.logger.log_info(f"유효한 유튜브 URL: {url}")
        return True