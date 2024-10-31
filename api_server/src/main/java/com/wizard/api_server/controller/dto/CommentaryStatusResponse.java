package com.wizard.api_server.controller.dto;

import lombok.Builder;

public class CommentaryStatusResponse {
    private String commentaryStatus;

    @Builder
    public CommentaryStatusResponse(String commentaryStatus) {
        this.commentaryStatus = commentaryStatus;
    }
}
