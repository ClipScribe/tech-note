package com.wizard.api_server.kafka.requestproducer.message;

import lombok.Builder;

public class CommentaryRequestMessage {
    private String requestId;
    private String youtubeLink;

    @Builder
    public CommentaryRequestMessage(String requestId, String youtubeLink) {
        this.requestId = requestId;
        this.youtubeLink = youtubeLink;
    }
}
