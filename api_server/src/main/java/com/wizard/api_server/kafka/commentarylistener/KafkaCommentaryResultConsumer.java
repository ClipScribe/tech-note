package com.wizard.api_server.kafka.commentarylistener;

import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

/**
 * 'transcription_results' 토픽의 메시지를 소비하고 처리하는 클래스
 */
@Service
@Slf4j
public class KafkaCommentaryResultConsumer {

    public KafkaCommentaryResultConsumer() {
    }

    /**
     * Kafka 메시지를 수신하여 처리하는 메서드
     *
     * @param message 수신된 메시지 (JSON 형식)
     */
    @KafkaListener(topics = "${kafka.topic.transcription-results}", groupId = "${spring.kafka.consumer.group-id}", containerFactory = "kafkaProgressListenerContainerFactory")
    public void consume(String message) {
        try {
            // 메시지를 JSON으로 파싱

            // requestId와 최종 트랜스크립션 텍스트 추출

            // 데이터베이스에서 해당 요청 조회

            // 트랜스크립션 결과 저장

            // 변경 사항 저장;

            // sse로 클라이언트로 전송


        } catch (Exception e) {

        }
    }
}