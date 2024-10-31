package com.wizard.api_server.kafka.requestproducer;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.wizard.api_server.controller.dto.CommentaryResponseDto;
import com.wizard.api_server.kafka.requestproducer.message.CommentaryRequestMessage;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

/**
 * Kafka로 메시지를 발행하는 프로듀서 클래스
 */
@Component
public class KafkaRequestProducer {

    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper;

    @Value("${kafka.topic.transcription-requests}")
    private String requestTopic;

    public KafkaRequestProducer(KafkaTemplate<String, String> kafkaTemplate, ObjectMapper objectMapper) {
        this.kafkaTemplate = kafkaTemplate;
        this.objectMapper = objectMapper;
    }

    /**
     * DTO를 JSON 문자열로 변환하여 지정된 토픽으로 전송
     * @param requestMessage CommentaryRequestMessage
     */
    public void sendMessage(CommentaryRequestMessage requestMessage) {
        try {
            String message = objectMapper.writeValueAsString(requestMessage);
            kafkaTemplate.send(requestTopic, message);
        } catch (JsonProcessingException e) {
            // 예외 처리 로직 (로깅 등)을 추가
            throw new RuntimeException("Failed to convert DTO to JSON", e);
        }
    }
}
