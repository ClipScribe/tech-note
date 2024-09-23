package com.wizard.api_server.external.kafka.producer;

import com.wizard.api_server.domain.event.DomainEvent;
import com.wizard.api_server.domain.event.DomainEventPublisher;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class VideoLinkProducer implements DomainEventPublisher {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Override
    public void publish(DomainEvent event) {
        String topic = "video-event";
        kafkaTemplate.send(topic, event);
    }
}
