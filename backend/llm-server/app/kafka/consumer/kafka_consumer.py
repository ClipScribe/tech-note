import time
import traceback

from loguru import logger

from app.domain.kafka_message.initiate_request_message import InitiateRequestMessage
from app.domain.kafka_message.stt_chunk_result_message import STTChunkResultMessage


from app.message_processor.message_processor import *
from app.text_utils.text_utils import TextMergerToFile



async def consume_initial_requests(consumer, producer ,initial_messages, assistants, processors):
    """
    초기 메시지를 소비하고 request_id별로 정보를 저장하는 함수.
    요청 처리가 완료되면 해당 request_id의 정보를 삭제합니다.

    Parameters:
        consumer: Kafka consumer 인스턴스
        initial_messages (dict): 초기 메시지를 저장하는 딕셔너리, key는 request_id
        assistants: assitant dic-> beginner, intermediate, expert
        processors: request_id별 processor를 생성해 stt_result consumer에서 사용하기 위한 목적
    """
    logger.info("초기 메시지를 소비하기 시작합니다.")

    try:
        async for msg in consumer:
            # InitialMessage로 메시지 파싱
            logger.info(f"Initial message consume: {msg.value}")
            initial_message = InitiateRequestMessage.model_validate_json(msg.value)

            request_id = initial_message.request_id

            # 초기 메시지를 딕셔너리에 저장
            initial_messages[request_id] = initial_message
            logger.info(f"Request ID '{request_id}'의 초기 메시지를 저장했습니다.")

            # processor를 생성
            match initial_message.explanation_level:
                case "beginner":
                    message_processor = MessageProcessor(
                        request_id=request_id,
                        assistant=assistants['beginner'],
                        explanation_level=initial_message.explanation_level,
                        producer=producer
                    )
                    processors[request_id] = message_processor
                case "intermediate":
                    message_processor = MessageProcessor(
                        request_id=request_id,
                        assistant=assistants['intermediate'],
                        explanation_level=initial_message.explanation_level,
                        producer=producer
                    )
                    processors[request_id] = message_processor
                case "expert":
                    message_processor = MessageProcessor(
                        request_id=request_id,
                        assistant=assistants['expert'],
                        explanation_level=initial_message.explanation_level,
                        producer=producer
                    )
                    processors[request_id] = message_processor


    except Exception as e:
        logger.error(f"초기 메시지 소비 중 오류 발생: {e}")
    finally:
        logger.info("초기 메시지 소비 종료.")

async def consume_stt_results(consumer, initial_messages, processors):
    """
    STT 결과물을 소비하고 텍스트를 재구성하여 병합하는 함수.
    각 request_id별로 메시지를 순서에 맞게 병합하여 원본 텍스트로 재구성하고,
    전체 chunk_id가 다 모이면 initial_messages에서 삭제.

    Parameters:
        consumer: Kafka consumer 인스턴스
        initial_messages (dict): request_id를 키로 초기 메시지 정보를 저장하는 딕셔너리
        processors: initial consumer에서 생성한 request_id 별 processor를 사용하기 위한 dict
    """
    logger.info("STT 결과물을 소비하기 시작합니다.")

    try:
        async for msg in consumer:
            # STTChunkResultMessage로 메시지 파싱
            logger.info(f"chunk message consume: {msg.value}")
            stt_result = STTChunkResultMessage.model_validate_json(msg.value)

            request_id = stt_result.request_id
            chunk_id = stt_result.chunk_id
            transcription_text = stt_result.transcription_text

            # initial_messages에 request_id가 없다면 새로 초기화
            if request_id not in initial_messages:
                logger.error(f"Request ID '{request_id}'에 대한 초기 정보가 존재하지 않습니다. 메시지를 스킵합니다.")
                continue
            else:
                initial_message = initial_messages[request_id]

            # 초기 메시지에서 전체 청크 개수 가져오기
            total_chunks = initial_messages[request_id].total_chunk_num

            #초기 파일 생성
            TextMergerToFile.initialize_file(request_id)

            # STT 메시지에서 텍스트를 추출하여 병합 파일에 추가
            TextMergerToFile.add_message(request_id, {"request_id": request_id, "chunk_id": chunk_id,
                                                      "transcription_text": transcription_text})
            logger.debug(f"Request ID '{request_id}', Chunk ID '{chunk_id}' 병합 처리 완료.")

            # 모든 청크가 처리되었는지 확인
            if chunk_id == total_chunks - 1:
                # 병합 완료 시 최종 텍스트를 로그에 표시
                logger.info(f"Request ID '{request_id}'의 모든 청크 병합이 완료되었습니다.")
                transcript_file_path = TextMergerToFile.get_merged_text(request_id)

                #initiate
                initial_thread, initial_vector_store = await message_processor.initiate(transcript_file_path)
                logger.info(f"thread{initial_thread.id}created")
                #목차 생성
                await message_processor.create_indices(initial_thread)

                #목차로 텍스트 파일 분할
                index_path = f"capstone_storage/{request_id}/index/index.txt"
                logger.info(index_path)
                transcription_chunks_path = TextMergerToFile.split_by_toc(request_id=request_id, toc_filepath=index_path)

                #목차별 설명문 생성
                chunk_resource_list = await message_processor.create_explanations(transcription_chunks_path)
                #목차별 설명문 피드백 수행
                await message_processor.create_feedbacks_for_explanations(chunk_resource_list)
                #목차별 피드백 반영 설명문 생성
                await message_processor.create_enhanced_explanations(chunk_resource_list)


    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"STT 결과물 소비 중 오류 발생: {e}\n세부 정보:\n{error_details}")
    finally:
        logger.info("STT 결과물 소비 종료.")






