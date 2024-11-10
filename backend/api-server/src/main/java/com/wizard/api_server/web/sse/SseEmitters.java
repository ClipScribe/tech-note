package com.wizard.api_server.web.sse;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@Slf4j
@Component
public class SseEmitters {
    private final Map<String, SseEmitter> emitters = new ConcurrentHashMap<>();

    public void addEmiter(String connectId, SseEmitter emitter) {
        emitters.put(connectId, emitter);
        log.info("Added emitter {}", connectId);;
        log.info("emitter list size: {}", emitters.size());

        emitter.onCompletion(() -> {
            log.info("emitter completed");
            emitters.remove(connectId);
        });

        emitter.onTimeout(() -> {
            log.info("emitter timed out");
            emitter.complete();
        });
    }

    public void sendConnectEvent(SseEmitter emitter) throws IOException {
            var event = SseEmitter.event()
                    .name("connect");
            emitter.send(event);
    }
}
