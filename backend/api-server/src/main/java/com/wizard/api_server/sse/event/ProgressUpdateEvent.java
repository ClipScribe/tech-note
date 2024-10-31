package com.wizard.api_server.sse.event;

import lombok.Builder;

public class ProgressUpdateEvent {
    //나중에 이벤트 전송 시 사용할 클래스
    //지금은 메서드에서 바로 이벤트를 전송

    private String eventName;
    private String message;

    @Builder
    public ProgressUpdateEvent(String eventName, String message) {
        this.eventName = eventName;
        this.message = message;
    }

    public String getEventName() {
        return eventName;
    }

    public String getMessage() {
        return message;
    }
}