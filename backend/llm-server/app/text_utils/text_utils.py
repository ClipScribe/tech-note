from loguru import logger
import re
import os

class TextMergerToFile:
    """
    텍스트 병합과 목차에 따른 파일 분할 기능을 제공하는 클래스.
    """

    @staticmethod
    def initialize_file(request_id):
        file_path = f"{request_id}.txt"
        with open(file_path, "w") as f:
            pass
        logger.info(f"Initialized text file at {file_path} for request_id '{request_id}'.")

    @staticmethod
    def add_message(request_id, message):
        """
        개별 STT 메시지에서 transcription_text를 추출하여 파일에 추가.

        Parameters:
            request_id (str): 요청 ID를 사용하여 파일 경로 생성
            message (dict): {'request_id': str, 'chunk_id': int, 'transcription_text': str} 형식의 메시지
        """
        transcription_text = message.get("transcription_text", "")
        file_path = f"{request_id}.txt"

        with open(file_path, "a") as f:
            f.write(transcription_text + " ")  # 메시지 뒤에 공백 추가

        logger.debug(f"Added transcription text to file {file_path}: {transcription_text[:50]}...")

    @staticmethod
    def get_merged_text(request_id):
        """
        지금까지 파일에 저장한 텍스트를 합쳐서 반환.

        Parameters:
            request_id (str): 요청 ID를 사용하여 파일 경로 생성

        Returns:
            str: 합쳐진 원본 텍스트
        """
        file_path = f"{request_id}.txt"
        with open(file_path, "r") as f:
            original_text = f.read().strip()

        logger.debug(f"Merged text (preview): {original_text[:50]}...")
        return original_text

    @staticmethod
    def split_by_toc(request_id, toc, output_folder):
        """
        타임스탬프와 목차를 기준으로 텍스트 파일을 분할하여 각 목차별 세부 파일을 생성.

        Parameters:
            request_id (str): 요청 ID를 사용하여 파일 경로 생성
            toc (list): 각 목차가 포함된 리스트. 예: [{'title': 'Introduction', 'start': 0.0, 'length': 60.0}, ...]
            output_folder (str): 분할된 파일을 저장할 폴더 경로
        """
        os.makedirs(output_folder, exist_ok=True)  # 출력 폴더 생성

        original_text = TextMergerToFile.get_merged_text(request_id)

        for index, item in enumerate(toc, start=1):
            title = item['title']
            start_time = item['start']
            length = item['length']
            end_time = start_time + length

            pattern = rf"({start_time}\s+\d+\.\d+\s+.+?)(?={end_time}\s+\d+\.\d+|$)"
            match = re.search(pattern, original_text, re.DOTALL)

            if match:
                segment_content = match.group(1).strip()
                output_file = f"{output_folder}/{request_id}_{index}.txt"

                with open(output_file, "w") as outfile:
                    outfile.write(f"Title: {title}\nStart: {start_time}\nLength: {length}\nContent:\n{segment_content}")

                logger.debug(f"Saved segment '{title}' from {start_time} to {end_time} in file {output_file}")
            else:
                logger.warning(f"No content found for TOC item '{title}' with timestamps {start_time}-{end_time}")

        logger.info("Text split by TOC and saved to separate files.")