import json
from datetime import datetime

from loguru import logger

from app.domain.kafka_message.initiate_request_message import InitiateRequestMessage
from app.domain.kafka_message.stt_chunk_result_message import STTChunkResultMessage
from app.domain.dto.chunk_message_dto import ChunkMessageDto
from app.orchestrator.orchestrator import *


async def consume_initial_requests(consumer, producer, processors):
    logger.info("초기 요청을 소비하기 시작합니다.")

    try:
        async for msg in consumer:
            # InitiateRequestMessage 클래스를 사용하여 메시지 파싱
            initiate_request = InitiateRequestMessage.model_validate_json(msg.value)
            request_id = initiate_request.request_id
            total_chunk_num = initiate_request.total_chunk_num
            explanation_level = initiate_request.explanation_level

            logger.info(f"초기 메시지 수신: request_id {request_id}")
            processors[request_id] = RequestProcessor(request_id=request_id, total_chunk_num=total_chunk_num, producer=producer)
            await processors[request_id].add_initial_message(explanation_level)

    except Exception as e:
        logger.error(f"초기 요청 소비 중 오류 발생: {e}")
    finally:
        logger.info("초기 요청 소비 종료.")


async def consume_stt_results(consumer, processors, assistant_id):
    logger.info("STT 결과물을 소비하기 시작합니다.")
    try:
        async for msg in consumer:
            # STTChunkResultMessage 클래스를 사용하여 메시지 파싱
            logger.info(f"chunk message consume: {msg.value}")
            stt_result = STTChunkResultMessage.model_validate_json(msg.value)
            request_id = stt_result.request_id
            chunk_id = stt_result.chunk_id
            timestamp = stt_result.timestamp
            content = stt_result.content

            # 일반 chunk 메시지를 DTO로 변환
            chunk_message = ChunkMessageDto(
                request_id=request_id,
                chunk_id=chunk_id,
                timestamp=timestamp,
                content=content
            )

            processor = processors[request_id]
            processor.add_message(chunk_message)

            # 메시지가 30개 이상 모였는지 확인 후 처리
            if processor.priority_message_queue.qsize() > 30:
                logger.info(f"30개 청크 단위로 segment 생성 시작: request_id {request_id}")
                segment = await processor.process_message_to_segment(batch_size=30)
                logger.info(f"30개 청크 단위로 segment 생성 끝: request_id {request_id}")
                await processor.run_stream(assistant_id=assistant_id, thread_id=processor.thread.id, segment_start_time=segment.start_time)
                logger.info(f"생성한 segment로 run_stream: request_id {request_id}")


            # 마지막 청크 확인 시 프로세서 삭제
            if processor.current_chunk_id >= processor.total_chunk_num:
                if not processor.priority_message_queue.empty():
                    logger.info(f"남은 chunk들로 segment 생성 및 실행: request_id {request_id}")
                    segment = await processor.process_message_to_segment(batch_size=30)
                    await processor.run_stream(assistant_id=assistant_id, thread_id=processor.thread.id, segment_start_time=segment.start_time)
                logger.info(f"모든 청크가 처리되었습니다: request_id {request_id}")
                processor.close_request()
                del processors[request_id]  # 메모리에서 제거

    except Exception as e:
        logger.error(f"STT 결과물 소비 중 오류 발생: {e}")
    finally:
        logger.info("STT 결과물 소비 종료.")






