package com.wizard.api_server.web.sse;

import java.io.IOException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@Slf4j
@RestController
@RequestMapping("/sse")
@RequiredArgsConstructor
public class SseController {
    private final SseEmitters emitters;

    @GetMapping("/connect/{connectId}")
    public SseEmitter connect(@PathVariable("connectId") String connectId){
        log.info("요청 받음 "+ connectId);
        SseEmitter emitter = new SseEmitter();
        emitters.addEmiter(connectId, emitter);

        try {
            log.info("Connecting to " + connectId);
            emitters.sendConnectEvent(emitter);
        } catch (IOException e) {
            log.info("SSE 연결 실패");
            throw new RuntimeException(e);
        }
        return emitter;
    }
}
