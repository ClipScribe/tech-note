package com.wizard.api_server.service;

import com.wizard.api_server.common.exception.customexceptions.CommentaryRequestCreationException;
import com.wizard.api_server.controller.ProgressController;
import com.wizard.api_server.controller.dto.CommentaryRequestDto;
import com.wizard.api_server.domain.entity.CommentaryRequest;
import com.wizard.api_server.kafka.requestproducer.KafkaRequestProducer;
import com.wizard.api_server.kafka.requestproducer.message.CommentaryRequestMessage;
import com.wizard.api_server.mapper.CommentaryRequestMapper;
import com.wizard.api_server.repository.CommentaryRequestRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

/**
 * CommentaryRequestService 구현 클래스
 */
@Service
@Slf4j
public class CommentaryRequestService {

    private CommentaryRequestRepository commentaryRequestRepository;

    private KafkaRequestProducer kafkaRequestProducer;

    public CommentaryRequestService(CommentaryRequestRepository commentaryRequestRepository, KafkaRequestProducer kafkaRequestProducer, ProgressController progressController) {}

    /**
     * 클라이언트로부터 받은 DTO를 엔티티로 변환하고, 저장 후 requestId를 반환
     * @param dto CommentaryRequestDto
     * @return UUID requestId
     */
    @Transactional
    public UUID createCommentaryRequest(CommentaryRequestDto dto) {
        try {
            // DTO를 엔티티로 매핑
            CommentaryRequest request = CommentaryRequestMapper.INSTANCE.toEntity(dto);
            CommentaryRequest savedRequest = commentaryRequestRepository.save(request);
            log.info("comment request saved: {}", savedRequest.getRequestId());

            // Kafka로 초기 메시지 발행
            CommentaryRequestMessage requestMessage = CommentaryRequestMapper.INSTANCE.toMessageDto(savedRequest);
            kafkaRequestProducer.sendMessage(requestMessage);
            log.info("comment request produced: {}", savedRequest.getRequestId());

            // 성공 시 requestId 반환
            return savedRequest.getRequestId();
        } catch (Exception e) {
            // 예외 로깅
            log.error("Failed to create commentary request", e);
            // 필요 시 롤백 또는 추가 예외 처리
            throw new CommentaryRequestCreationException("Failed to create commentary request", e);
        }
    }
}