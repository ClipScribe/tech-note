package com.wizard.api_server.domain.event;

import java.util.UUID;

public interface DomainEvent {
    UUID getEventId();
}
