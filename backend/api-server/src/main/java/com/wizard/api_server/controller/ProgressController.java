package com.wizard.api_server.controller;

import com.wizard.api_server.sse.CommentaryProgressSseService;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.UUID;

/**
 * 진행 상황을 클라이언트에 실시간으로 전송하기 위한 컨트롤러
 * Server-Sent Events (SSE)를 사용하여 단방향 스트리밍을 제공
 */
@RestController
@RequestMapping("/api/v1/videos")
public class ProgressController {

    private final CommentaryProgressSseService progressSseService;

    public ProgressController(CommentaryProgressSseService progressSseService) {
        this.progressSseService = progressSseService;
    }

    /**
     * 특정 requestId에 대한 진행 상황 스트림을 생성하고 클라이언트와 SSE 연결을 설정
     *
     * @param requestId 클라이언트가 구독할 비디오 요청의 UUID
     * @return SseEmitter 객체
     */
    @GetMapping(value = "/commentary/{requestId}", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter streamProgress(@PathVariable UUID requestId) {
        return progressSseService.createEmitter(requestId);
    }
}
