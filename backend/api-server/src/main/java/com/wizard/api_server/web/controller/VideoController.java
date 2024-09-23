package com.wizard.api_server.web.controller;

import com.wizard.api_server.domain.video.service.VideoService;
import com.wizard.api_server.web.dto.VideoLinkRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/video/link")
@RequiredArgsConstructor
public class VideoController {
    private final VideoService videoService;
    // 비디오 해설 생성 요청
    @PostMapping
    public ResponseEntity<Void> start(@RequestBody VideoLinkRequest request) {
        String videoLink = request.videoLink();
        // 비디오 링크 받아서 produce
        videoService.sendVideoLink(videoLink);
        // 처리 성공시
        return ResponseEntity.status(HttpStatus.OK).build();
    }
}
