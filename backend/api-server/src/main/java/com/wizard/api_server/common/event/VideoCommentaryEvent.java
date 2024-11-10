package com.wizard.api_server.common.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class VideoCommentaryEvent extends ApplicationEvent {

    private final String requestId;
    private final String content;
    private final long startTime;

    public VideoCommentaryEvent(Object source, String requestId, String content, long startTime) {
        super(source);
        this.requestId = requestId;
        this.content = content;
        this.startTime = startTime;
    }
}
