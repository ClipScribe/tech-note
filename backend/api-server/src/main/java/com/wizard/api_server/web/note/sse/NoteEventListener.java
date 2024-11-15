package com.wizard.api_server.web.note.sse;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.wizard.api_server.common.event.CreateNoteEvent;
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
public class NoteEventListener {
    private final ObjectMapper objectMapper;
    private final SseEmitters sseEmitters;

    @EventListener
    public void handleCreateNoteContentEvent(CreateNoteEvent event) {
        try {
            log.info("Received create note content event: {}", objectMapper.writeValueAsString(event));
            Map<String, Object> eventData = new HashMap<>();
            eventData.put("startTime", event.getStartTime());
            eventData.put("content", event.getContent());
            String jsonData = objectMapper.writeValueAsString(eventData);
            sseEmitters.sendEvent(event.getVideoId(),jsonData);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
