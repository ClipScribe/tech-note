package com.wizard.api_server.web.note.sse;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@Slf4j
@Component
public class SseEmitters {
    private final Map<String, SseEmitter> emitters = new ConcurrentHashMap<>();

    public void addEmiter(String connectId, SseEmitter emitter) {
        if(emitters.containsKey(connectId)) {
            log.info("Emitter already exist for connectId {}", connectId);
            return;
        }
        emitters.put(connectId, emitter);

        log.info("Added emitter {}", connectId);
        log.info("emitter list size: {}", emitters.size());

        emitter.onCompletion(() -> {
            log.info("emitter completed");
            emitters.remove(connectId);
        });

        emitter.onTimeout(() -> {
            log.info("emitter timed out");
            emitters.remove(connectId);
        });
        emitter.onError((error) -> {
            log.error("Error occurred for connectId: {}", connectId, error);
        });
    }

    public void sendConnectEvent(SseEmitter emitter) throws IOException {
        var event = SseEmitter.event()
                    .name("connect")
                            .data("send connect event");
            emitter.send(event);
        log.info("emitter sent first event");
    }

    public void sendEvent(String requestId, String data) throws IOException {
        SseEmitter emitter = emitters.get(requestId);
        if (emitter != null) {
            var event = SseEmitter.event()
                    .name("commentary")
                    .data(data);

            emitter.send(event, MediaType.APPLICATION_JSON);
            log.info("emitter sent comment event");
        } else {
            log.warn("emitter not found");
        }
    }

    public Map<String, SseEmitter> getEmitters() {
        return emitters;
    }
    /**
     *   {"requestId": "3ddfd9be-3896-41d3-a8d1-97e1e33c623f", "startTime": 0, "content": "# This is a commentary about the note."}
     */
}
