package com.wizard.api_server.common.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class CreateNoteEvent extends ApplicationEvent {

    private final String videoId;
    private final long startTime;
    private final String content;

    public CreateNoteEvent(Object source, String videoId, long startTime, String content) {
        super(source);
        this.videoId = videoId;
        this.startTime = startTime;
        this.content = content;
    }
}
