package com.wizard.api_server.web.sse;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.wizard.api_server.common.event.VideoCommentaryEvent;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class VideoCommentaryEventListener {
    private final ObjectMapper objectMapper;
    private final SseEmitters sseEmitters;

    @EventListener
    public void handleVideoCommentaryEvent(VideoCommentaryEvent event) {
        try {
            log.info("Received video commentary event: {}", objectMapper.writeValueAsString(event));
            Map<String, Object> eventData = new HashMap<>();
            eventData.put("startTime", event.getStartTime());
            eventData.put("content", event.getContent());
            String jsonData = objectMapper.writeValueAsString(eventData);
            sseEmitters.sendEvent(event.getRequestId(),jsonData);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
