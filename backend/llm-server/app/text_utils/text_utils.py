import json
import sys

from loguru import logger
import re
import os

class TextMergerToFile:
    """
    텍스트 병합과 목차에 따른 파일 분할 기능을 제공하는 클래스.
    """

    @staticmethod
    def initialize_file(request_id):
        # 디렉토리 경로와 파일 경로 설정
        dir_path = f"capstone_storage/{request_id}"
        file_path = f"{dir_path}/original_{request_id}.txt"

        # 디렉토리가 없으면 생성
        os.makedirs(dir_path, exist_ok=True)

        # 파일 생성
        with open(file_path, "w") as f:
            pass  # 빈 파일 생성

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
        file_path = f"capstone_storage/{request_id}/original_{request_id}.txt"

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
        file_path = f"capstone_storage/{request_id}/original_{request_id}.txt"  # 경로 수정
        with open(file_path, "r") as f:
            original_text = f.read().strip()

        logger.debug(f"Merged text (preview): {original_text[:50]}...")
        return file_path

    """
    @staticmethod
    def split_by_toc(request_id, toc_filepath):
        output_folder = f"capstone_storage/{request_id}/transcription_chunks"
        os.makedirs(output_folder, exist_ok=True)
        logger.info(f"Output folder '{output_folder}' created or already exists.")

        # TOC 파일이 존재하는지, 비어있지 않은지 확인
        if not os.path.exists(toc_filepath):
            logger.error(f"TOC file '{toc_filepath}' does not exist.")
            return
        elif os.path.getsize(toc_filepath) == 0:
            logger.error(f"TOC file '{toc_filepath}' is empty.")
            return

        # TOC 파일을 텍스트로 로드하고 항목 추출
        try:
            with open(toc_filepath, 'r', encoding='utf-8') as toc_file:
                toc_text = toc_file.read()
                logger.info(f"TOC text file '{toc_filepath}' loaded successfully.")
                logger.debug(toc_text)
        except Exception as e:
            logger.error(f"Error loading TOC file: {e}")
            return

        # TOC 항목 정규식 패턴
        pattern = r'"start_time":\s*"([\d.]+)",\s*"index":\s*"(.*?)"'
        toc = re.findall(pattern, toc_text)
        logger.debug(toc)

        # 분할할 원본 텍스트 데이터 로드
        text_data_path = f"capstone_storage/{request_id}/original_{request_id}.txt"
        try:
            with open(text_data_path, 'r', encoding='utf-8') as text_file:
                text_data = json.load(text_file)
                logger.info(f"Original text data loaded from '{text_data_path}'.")
        except Exception as e:
            logger.error(f"Error loading text data file: {e}")
            return

        # 각 TOC 항목에 대해 텍스트 분할 및 파일 저장
        for i, (timestamp, title) in enumerate(toc):
            # start_time과 end_time 설정
            try:
                start_time = float(timestamp)
                end_time = float(toc[i + 1][0]) if i + 1 < len(toc) else None
                index_num = i + 1  # 파일명에 사용할 인덱스 번호

                # 디버그 로그: 현재 TOC 항목의 시작 시간과 종료 시간 출력
                logger.debug(f"Processing TOC item '{title}' (start_time: {start_time}, end_time: {end_time})")
            except Exception as e:
                logger.error(f"Error parsing start or end time for TOC item '{title}': {e}")
                continue

            # start_time과 end_time 범위에 속하는 텍스트 찾기
            segment_content = []
            for text_item in text_data:
                try:
                    text_start = float(text_item['start'])
                    # 조건을 만족하는지 여부와 start 시간 로그 출력
                    logger.debug(f"Checking text item with start: {text_start}, text: {text_item['text'][:50]}")

                    if text_start >= start_time and (end_time is None or text_start < end_time):
                        segment_content.append(text_item['text'])
                        logger.info(f"Added segment: {text_item['text'][:50]}...")  # 추가된 텍스트의 첫 50자 미리보기 출력
                except Exception as e:
                    logger.error(f"Error processing text item: {e}")
                    continue
            # 분할된 텍스트 파일에 쓰기
            if segment_content:
                try:
                    output_file = f"{output_folder}/{request_id}_{index_num}.txt"
                    with open(output_file, "w", encoding="utf-8") as outfile:
                        outfile.write(f"Title: {title}\nStart: {start_time}\nContent:\n" + "\n".join(segment_content))
                    logger.info(f"Saved segment '{title}' in file {output_file}")
                except IOError as e:
                    logger.error(f"Failed to write file {output_file}: {e}")
            else:
                logger.warning(f"No content found for TOC item '{title}' with start time {start_time}")

        logger.info("Text split by TOC and saved to separate files.")
        return output_folder
    """

    """
    @staticmethod
    def split_by_toc(request_id, toc_filepath):
        output_folder = f"capstone_storage/{request_id}/transcription_chunks"
        os.makedirs(output_folder, exist_ok=True)
        logger.info(f"Output folder '{output_folder}' created or already exists.")

        # TOC 파일이 존재하는지, 비어있지 않은지 확인
        if not os.path.exists(toc_filepath):
            logger.error(f"TOC file '{toc_filepath}' does not exist.")
            return
        elif os.path.getsize(toc_filepath) == 0:
            logger.error(f"TOC file '{toc_filepath}' is empty.")
            return

        # TOC 파일을 JSON 형식으로 로드
        try:
            with open(toc_filepath, 'r', encoding='utf-8') as toc_file:
                toc_data = json.load(toc_file)  # JSON 파일을 파싱하여 Python 객체로 로드
                logger.info(f"TOC JSON file '{toc_filepath}' loaded successfully.")
                logger.debug(toc_data)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding TOC JSON file '{toc_filepath}': {e}")
            return
        except Exception as e:
            logger.error(f"Error loading TOC file: {e}")
            return

        # TOC 데이터의 'indices' 항목 가져오기
        indices = toc_data.get("indices", [])
        if not indices:
            logger.error("No 'indices' found in TOC JSON file.")
            return

        # 분할할 원본 텍스트 데이터 로드
        text_data_path = f"capstone_storage/{request_id}/original_{request_id}.json"
        try:
            with open(text_data_path, 'r', encoding='utf-8') as text_file:
                text_data = json.load(text_file)
                logger.info(f"Original text data loaded from '{text_data_path}'.")
        except Exception as e:
            logger.error(f"Error loading text data file: {e}")
            return

        # 각 TOC 항목에 대해 텍스트 분할 및 파일 저장
        for i, toc_item in enumerate(indices):
            try:
                start_time = float(toc_item['start_time'])
                end_time = float(indices[i + 1]['start_time']) if i + 1 < len(indices) else None
                title = toc_item['index']
                index_num = i + 1  # 파일명에 사용할 인덱스 번호

                # 디버그 로그: 현재 TOC 항목의 시작 시간과 종료 시간 출력
                logger.debug(f"Processing TOC item '{title}' (start_time: {start_time}, end_time: {end_time})")
            except Exception as e:
                logger.error(f"Error parsing start or end time for TOC item '{title}': {e}")
                continue

            # start_time과 end_time 범위에 속하는 텍스트 찾기
            segment_content = []
            for text_item in text_data:
                try:
                    text_start = float(text_item['start'])
                    logger.debug(f"Checking text item with start: {text_start}, text: {text_item['text'][:50]}")

                    if text_start >= start_time and (end_time is None or text_start < end_time):
                        segment_content.append(text_item['text'])
                        logger.info(f"Added segment: {text_item['text'][:50]}...")  # 추가된 텍스트의 첫 50자 미리보기 출력
                except Exception as e:
                    logger.error(f"Error processing text item: {e}")
                    continue

            # 분할된 텍스트 파일에 쓰기
            if segment_content:
                try:
                    output_file = f"{output_folder}/{request_id}_{index_num}.txt"
                    with open(output_file, "w", encoding="utf-8") as outfile:
                        outfile.write(f"Title: {title}\nStart: {start_time}\nContent:\n" + "\n".join(segment_content))
                    logger.info(f"Saved segment '{title}' in file {output_file}")
                except IOError as e:
                    logger.error(f"Failed to write file {output_file}: {e}")
            else:
                logger.warning(f"No content found for TOC item '{title}' with start time {start_time}")

        logger.info("Text split by TOC and saved to separate files.")
        return output_folder
    """
    """
    @staticmethod
    def split_by_toc(request_id, toc_filepath):
        output_folder = f"capstone_storage/{request_id}/transcription_chunks"
        os.makedirs(output_folder, exist_ok=True)
        logger.info(f"Output folder '{output_folder}' created or already exists.")

        # TOC 파일이 존재하는지, 비어있지 않은지 확인
        if not os.path.exists(toc_filepath):
            logger.error(f"TOC file '{toc_filepath}' does not exist.")
            return
        elif os.path.getsize(toc_filepath) == 0:
            logger.error(f"TOC file '{toc_filepath}' is empty.")
            return

        # TOC 파일을 텍스트로 로드한 후 ` ```json `과 같은 불필요한 문자 제거
        try:
            with open(toc_filepath, 'r', encoding='utf-8') as toc_file:
                toc_text = toc_file.read().strip()  # 앞뒤 공백 제거

                # 디버깅 로그: 파일 내용 미리보기
                logger.debug(f"TOC file content preview: {toc_text[:100]}")

                # 파일 내용이 비어있는지 확인
                if not toc_text:
                    logger.error(f"TOC file '{toc_filepath}' is empty after reading.")
                    return

                # ```json과 ``` 같은 불필요한 문자 제거
                toc_text = re.sub(r"```json|```", "", toc_text).strip()

                # JSON 파싱 시도
                toc_data = json.loads(toc_text)
                logger.info(f"TOC JSON file '{toc_filepath}' loaded successfully.")
                logger.debug(f"Parsed TOC data: {toc_data}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding TOC JSON file '{toc_filepath}': {e}")
            return
        except Exception as e:
            logger.error(f"Error loading TOC file: {e}")
            return

        # TOC 데이터의 'indices' 항목 가져오기
        indices = toc_data.get("indices", [])
        if not indices:
            logger.error("No 'indices' found in TOC JSON file.")
            return

        # 분할할 원본 텍스트 데이터 로드
        text_data_path = f"capstone_storage/{request_id}/original_{request_id}.txt"
        try:
            with open(text_data_path, 'r', encoding='utf-8') as text_file:
                text_data = json.load(text_file)
                logger.info(f"Original text data loaded from '{text_data_path}'.")
        except Exception as e:
            logger.error(f"Error loading text data file: {e}")
            return

        # 각 TOC 항목에 대해 텍스트 분할 및 파일 저장
        for i, toc_item in enumerate(indices):
            try:
                start_time = float(toc_item['start_time'])
                end_time = float(indices[i + 1]['start_time']) if i + 1 < len(indices) else None
                title = toc_item['index']
                summary = toc_item.get('summary', "")
                index_num = i + 1  # 파일명에 사용할 인덱스 번호

                # 디버그 로그: 현재 TOC 항목의 시작 시간과 종료 시간 출력
                logger.debug(f"Processing TOC item '{title}' (start_time: {start_time}, end_time: {end_time})")
            except Exception as e:
                logger.error(f"Error parsing start or end time for TOC item '{title}': {e}")
                continue

            # start_time과 end_time 범위에 속하는 텍스트 찾기
            segment_content = []
            for text_item in text_data:
                try:
                    text_start = float(text_item['start'])
                    logger.debug(f"Checking text item with start: {text_start}, text: {text_item['text'][:50]}")

                    if text_start >= start_time and (end_time is None or text_start < end_time):
                        segment_content.append(text_item['text'])
                        logger.info(f"Added segment: {text_item['text'][:50]}...")  # 추가된 텍스트의 첫 50자 미리보기 출력
                except Exception as e:
                    logger.error(f"Error processing text item: {e}")
                    continue

            # 분할된 텍스트 파일에 쓰기
            if segment_content:
                try:
                    output_file = f"{output_folder}/{request_id}_{index_num}.txt"
                    with open(output_file, "w", encoding="utf-8") as outfile:
                        outfile.write(
                            f"Title: {title}\nStart: {start_time}\nSummary: {summary}\nContent:\n" + "\n".join(
                                segment_content))
                    logger.info(f"Saved segment '{title}' in file {output_file}")
                except IOError as e:
                    logger.error(f"Failed to write file {output_file}: {e}")
            else:
                logger.warning(f"No content found for TOC item '{title}' with start time {start_time}")

        logger.info("Text split by TOC and saved to separate files.")
        return output_folder
    """

    @staticmethod
    def split_by_toc(request_id, toc_filepath):
        logger.info(toc_filepath)
        output_folder = f"capstone_storage/{request_id}/transcription_chunks"
        os.makedirs(output_folder, exist_ok=True)
        logger.info(f"Output folder '{output_folder}' created or already exists.")

        # TOC 파일 확인 및 로드
        if not os.path.exists(toc_filepath) or os.path.getsize(toc_filepath) == 0:
            logger.error(f"TOC file '{toc_filepath}' does not exist or is empty.")
            return None

        # TOC 파일 로드 및 불필요한 문자 제거 후 파싱
        try:
            with open(toc_filepath, 'r', encoding='utf-8') as toc_file:
                toc_text = toc_file.read()
                toc_text = re.sub(r"```json|```", "", toc_text)
                logger.info(toc_text)
                if not toc_text:
                    logger.error(f"TOC file '{toc_filepath}' has no valid JSON content after cleanup.")
                    return None
                toc_data = json.loads(toc_text)
                logger.info(f"TOC JSON file '{toc_filepath}' loaded successfully.")
                logger.info(toc_data)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding TOC JSON file '{toc_filepath}': {e}")
            return None

        # 분할할 원본 텍스트 데이터 로드 (이전 방식 유지)
        text_data_path = f"capstone_storage/{request_id}/original_{request_id}.txt"
        json_objects = []

        with open(text_data_path, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = r'\{[^{}]*\}'

        matches = re.findall(pattern, content)

        # 각 매칭된 JSON 객체를 파싱
        for match in matches:
            try:
                json_object = json.loads(match)
                json_objects.append(json_object)
            except json.JSONDecodeError as e:
                print(f"JSON decoding error in match: {match}, error: {e}")

        # TOC 항목에 따른 텍스트 분할 및 저장
        for i, toc_item in enumerate(toc_data):
            start_time = float(toc_item['start_time'])
            end_time = float(toc_data[i + 1]['start_time']) if i + 1 < len(toc_data) else sys.float_info.max
            title = toc_item['index']
            summary = toc_item.get('summary', "")
            index_num = i + 1

            segment_content = []

            for text_item in json_objects:
                text_start = float(text_item.get('start'))
                logger.info(f"toc_start_time : {start_time}, toc_end_time : {end_time}")
                logger.info(f"text_start_time : {text_start}")
                if start_time <= text_start <= end_time:
                    segment_content.append(text_item['text'])
                    logger.info(f"Added segment: {text_item['text'][:50]}...")

            if segment_content:
                output_file = os.path.join(output_folder, f"{request_id}_{index_num}.txt")
                try:
                    with open(output_file, "w", encoding="utf-8") as outfile:
                        outfile.write(
                            f"Title: {title}\nStart: {start_time}\nSummary: {summary}\nContent:\n" + "\n".join(
                                segment_content))
                    logger.info(f"Saved segment '{title}' in file {output_file}")
                except IOError as e:
                    logger.error(f"Failed to write file {output_file}: {e}")
            else:
                logger.warning(f"No content found for TOC item '{title}' with start time {start_time}")

        logger.info("Text split by TOC and saved to separate files.")
        return output_folder