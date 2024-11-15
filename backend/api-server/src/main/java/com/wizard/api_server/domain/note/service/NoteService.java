package com.wizard.api_server.domain.note.service;

import com.wizard.api_server.domain.note.event.CreateNoteEvent;
import com.wizard.api_server.domain.note.event.NoteEventPublisher;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class NoteService {
    private final NoteEventPublisher eventPublisher;

    public void sendVideoLink(String videoLink, String userLevel) {
        CreateNoteEvent event = new CreateNoteEvent(videoLink, userLevel);
        eventPublisher.publish(event);
    }
}
