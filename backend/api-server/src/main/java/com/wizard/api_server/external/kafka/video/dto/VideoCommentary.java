package com.wizard.api_server.external.kafka.video.dto;

public record VideoCommentary(
        String requestId,
        long startTime,
        String content) {
}
