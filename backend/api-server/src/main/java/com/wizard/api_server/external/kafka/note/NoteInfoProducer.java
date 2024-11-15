package com.wizard.api_server.external.kafka.note;

import com.wizard.api_server.domain.event.DomainEvent;
import com.wizard.api_server.domain.note.event.NoteEventPublisher;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class NoteInfoProducer implements NoteEventPublisher {
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Override
    public void publish(DomainEvent event) {
        String topic = "video-link-events";
        kafkaTemplate.send(topic, event);
    }
}
