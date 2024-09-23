package com.wizard.api_server.domain.event;

import java.time.LocalDateTime;
import java.util.UUID;

public interface DomainEvent {
    UUID getEventId();
    LocalDateTime getTimestamp();
}
