package com.wizard.api_server.domain.event;

public interface DomainEventPublisher {
    void publish(DomainEvent event);
}