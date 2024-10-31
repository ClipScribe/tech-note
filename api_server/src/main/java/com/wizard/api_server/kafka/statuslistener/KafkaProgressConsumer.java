package com.wizard.api_server.kafka.statuslistener;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.wizard.api_server.sse.CommentaryProgressSseService;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.UUID;

/**
 * Kafka에서 메시지를 수신하고 진행 상황을 클라이언트로 전송하는 소비자 클래스
 */
@Component
public class KafkaProgressConsumer {

    private final ObjectMapper objectMapper;

    private final CommentaryProgressSseService commentaryProgressSseService;

    public KafkaProgressConsumer(ObjectMapper objectMapper, CommentaryProgressSseService commentaryProgressSseService) {
        this.objectMapper = objectMapper;
        this.commentaryProgressSseService = commentaryProgressSseService;
    }

    /**
     * Kafka 토픽에서 메시지를 수신하여 처리
     * @param message 수신된 메시지
     */
    @KafkaListener(topics = "${kafka.topic.transcription-progress-updates}", groupId = "${spring.kafka.consumer.group-id}", containerFactory = "kafkaProgressListenerContainerFactory")
    public void listenTranscriptProgress(String message) {
        try {
            // 메시지를 JSON으로 파싱
            JsonNode jsonNode = objectMapper.readTree(message);
            UUID requestId = UUID.fromString(jsonNode.get("requestId").asText());
            String status = jsonNode.get("status").asText();
            Integer progress = jsonNode.get("progress").asInt();

            // 상태와 퍼센테이지를 메시지 형식으로 구성
            String progressMessage = String.format("%s 진행 중 %d/100", status, progress);

            // SSE로 전송
            commentaryProgressSseService.sendProgressUpdate(requestId, progressMessage);
        } catch (Exception e) {
            // 예외 처리 로직 (로깅 등)을 추가
            e.printStackTrace();
        }
    }

    /**
     * Kafka 토픽에서 메시지를 수신하여 처리
     * @param message 수신된 메시지
     */
    @KafkaListener(topics = "${kafka.topic.commentary-progress-updates}", groupId = "${spring.kafka.consumer.group-id}", containerFactory = "kafkaProgressListenerContainerFactory")
    public void listenCommentaryGenerationProgress(String message) {
        try {
            // 메시지를 JSON으로 파싱
            JsonNode jsonNode = objectMapper.readTree(message);
            UUID requestId = UUID.fromString(jsonNode.get("requestId").asText());
            String status = jsonNode.get("status").asText();
            Integer progress = jsonNode.get("progress").asInt();

            // 상태와 퍼센테이지를 메시지 형식으로 구성
            String progressMessage = String.format("%s 진행 중 %d/100", status, progress);

            // SSE로 전송
            commentaryProgressSseService.sendProgressUpdate(requestId, progressMessage);
        } catch (Exception e) {
            // 예외 처리 로직 (로깅 등)을 추가
            e.printStackTrace();
        }
    }
}
