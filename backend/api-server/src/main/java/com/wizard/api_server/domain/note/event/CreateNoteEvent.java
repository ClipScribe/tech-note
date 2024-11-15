package com.wizard.api_server.domain.note.event;

import com.wizard.api_server.domain.event.DomainEvent;

public record CreateNoteEvent(
    String videoId,
    String userLevel
) implements DomainEvent {
    @Override
    public String getEventId() {
        return videoId;
    }
}