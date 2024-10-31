package com.wizard.api_server.sse;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
@Slf4j
public class CommentaryProgressSseService {

    // requestId(UUID)와 해당하는 SseEmitter를 매핑하는 ConcurrentHashMap
    private final ConcurrentHashMap<UUID, SseEmitter> emitters = new ConcurrentHashMap<>();

    /**
     * 특정 requestId에 대한 SSE 연결을 생성하고 관리
     *
     * @param requestId 클라이언트가 구독할 비디오 요청의 UUID
     * @return 생성된 SseEmitter 객체
     */
    public SseEmitter createEmitter(UUID requestId) {
        // SseEmitter 생성 (타임아웃 설정)->나중에 적절한 타임아웃 시간 설정
        SseEmitter emitter = new SseEmitter(Long.MAX_VALUE);

        // emitters 맵에 추가
        emitters.put(requestId, emitter);

        // 클라이언트 연결이 완료되거나 타임아웃, 오류가 발생하면 emitters 맵에서 제거
        emitter.onCompletion(() -> emitters.remove(requestId));
        emitter.onTimeout(() -> {
            emitters.remove(requestId);
            emitter.complete();
        });
        emitter.onError((e) -> {
            emitters.remove(requestId);
            emitter.completeWithError(e);
            // 로깅 등을 통해 예외를 기록할 수 있습니다.
            log.info(e.getMessage());
        });

        return emitter;
    }

    /**
     * 특정 requestId에 대한 진행 상황 업데이트를 클라이언트에 전송
     *
     * @param requestId 진행 상황을 전송할 비디오 요청의 UUID
     * @param message   진행 상황 메시지 (예: "STT 진행 중 50/100")
     */
    public void sendProgressUpdate(UUID requestId, String message) {
        // requestId에 해당하는 SseEmitter를 가져옵니다.
        SseEmitter emitter = emitters.get(requestId);
        if (emitter != null) {
            try {
                // 'progress' 이벤트 이름으로 메시지를 전송합니다.
                emitter.send(SseEmitter.event()
                        .name("progress")
                        .data(message));
            } catch (Exception e) {
                // 전송 중 예외가 발생하면 emitters 맵에서 제거하고 emitter를 완료합니다.
                emitters.remove(requestId);
                emitter.completeWithError(e);
                // 로깅 등을 통해 예외를 기록할 수 있습니다.
                log.info(e.getMessage());
            }
        }
    }
}
