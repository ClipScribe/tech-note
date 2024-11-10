package com.wizard.api_server.external.kafka.video;

import com.wizard.api_server.domain.event.DomainEvent;
import com.wizard.api_server.domain.video.event.VideoEventPublisher;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class VideoLinkProducer implements VideoEventPublisher {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Override
    public void publish(DomainEvent event) {
        String topic = "video-link-events";
        kafkaTemplate.send(topic, event);
    }
}
