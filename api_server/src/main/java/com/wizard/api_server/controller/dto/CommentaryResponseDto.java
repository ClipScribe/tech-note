package com.wizard.api_server.controller.dto;

import com.wizard.api_server.domain.RequestStatus;
import lombok.Builder;

import java.util.UUID;

public class CommentaryResponseDto {
    private String requestId;

    @Builder
    public CommentaryResponseDto(UUID requestId) {
        this.requestId = requestId.toString();
    }
}
