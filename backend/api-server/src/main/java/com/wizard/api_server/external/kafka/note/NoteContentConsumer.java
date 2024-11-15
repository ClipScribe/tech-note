package com.wizard.api_server.external.kafka.note;

import com.wizard.api_server.common.event.CreateNoteEvent;
import com.wizard.api_server.external.kafka.note.dto.NoteContent;
import lombok.RequiredArgsConstructor;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class NoteContentConsumer {

    private final ApplicationEventPublisher eventPublisher;

    @KafkaListener(
            topics = "llm-commentary-events",
            groupId = "group_1",
            containerFactory = "kafkaListenerContainerFactory"
    )
    public void listenToNoteContent(NoteContent noteContent) {
        System.out.println("received note content");
        System.out.println("videoId: " + noteContent.videoId());
        System.out.println("startTime: " + noteContent.startTime());
        System.out.println("content: " + noteContent.content());

        CreateNoteEvent event = new CreateNoteEvent(
                this,
                noteContent.videoId(),
                noteContent.startTime(),
                noteContent.content()
        );
        eventPublisher.publishEvent(event);
    }
}
