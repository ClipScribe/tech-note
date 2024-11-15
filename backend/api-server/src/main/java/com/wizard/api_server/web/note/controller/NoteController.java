package com.wizard.api_server.web.note.controller;

import com.wizard.api_server.domain.note.service.NoteService;
import com.wizard.api_server.web.note.dto.CreateNoteRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/notes")
@RequiredArgsConstructor
public class NoteController {
    private final NoteService videoService;
    // 비디오 해설 생성 요청
    @PostMapping("")
    public ResponseEntity<Void> start(@RequestBody CreateNoteRequest request) {
        String videoId = request.videoId();
        String userLevel = request.userLevel();
        videoService.sendVideoLink(videoId, userLevel);
        return ResponseEntity.status(HttpStatus.OK).build();
    }
}
