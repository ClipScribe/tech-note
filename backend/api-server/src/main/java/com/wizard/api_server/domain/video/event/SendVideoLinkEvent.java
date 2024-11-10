package com.wizard.api_server.domain.video.event;

import com.wizard.api_server.domain.event.DomainEvent;
import java.util.UUID;

public record SendVideoLinkEvent (
    UUID eventId,
    String videoLink
) implements DomainEvent {
    public SendVideoLinkEvent(String videoLink) {
        this(UUID.randomUUID(), videoLink);
    }

    @Override
    public UUID getEventId() {
        return eventId;
    }
}