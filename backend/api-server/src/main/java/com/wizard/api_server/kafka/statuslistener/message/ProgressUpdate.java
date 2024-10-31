package com.wizard.api_server.kafka.statuslistener.message;

import com.wizard.api_server.domain.RequestStatus;
import lombok.Builder;

import java.util.UUID;

public class ProgressUpdate {
    private UUID requestId;
    private RequestStatus status;
    private int taskProgress;

    @Builder
    public ProgressUpdate(UUID requestId, RequestStatus status, int taskProgress) {
        this.requestId = requestId;
        this.status = status;
        this.taskProgress = taskProgress;
    }
}
