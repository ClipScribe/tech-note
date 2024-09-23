package com.wizard.api_server.domain.video.event;

import com.wizard.api_server.domain.event.DomainEvent;
import java.time.LocalDateTime;
import java.util.UUID;

public record SendVideoLinkEvent (
    UUID eventId,
    LocalDateTime timestamp,
    String videoLink
) implements DomainEvent {
    public SendVideoLinkEvent(String videoLink) {
        this(UUID.randomUUID(), LocalDateTime.now(), videoLink);
    }

    @Override
    public UUID getEventId() {
        return eventId;
    }

    @Override
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
}

