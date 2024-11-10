package com.wizard.api_server.external.kafka.video;

import com.wizard.api_server.external.kafka.video.dto.VideoCommentary;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class VideoCommentaryConsumer {

    @KafkaListener(
            topics = "llm-commentary-events",
            groupId = "group_1",
            containerFactory = "kafkaListenerContainerFactory"
    )
    public void listenToVideoSummary(VideoCommentary videoSummary) {
        System.out.println("Received Video Summary:");
        System.out.println("Request ID: " + videoSummary.requestId());
        System.out.println("Timestamp: " + videoSummary.startTime());
        System.out.println("Content: " + videoSummary.content());
    }
}
