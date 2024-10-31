package com.wizard.api_server.controller;

import com.wizard.api_server.common.response.ApiResponse;
import com.wizard.api_server.controller.dto.CommentaryRequestDto;
import com.wizard.api_server.controller.dto.CommentaryResponseDto;
import com.wizard.api_server.service.CommentaryRequestService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.UUID;

@Controller
@RequestMapping("/api/commentary")
public class CommentaryGenerationController {

    private final CommentaryRequestService commentaryRequestService;

    public CommentaryGenerationController(CommentaryRequestService commentaryRequestService) {
        this.commentaryRequestService = commentaryRequestService;
    }

    @PostMapping("/create")
    public ResponseEntity<ApiResponse<CommentaryResponseDto>> createCommentaryRequest(@Valid @RequestBody CommentaryRequestDto commentaryRequestDto) {
        UUID requestId = commentaryRequestService.createCommentaryRequest(commentaryRequestDto);
        CommentaryResponseDto responseDto = CommentaryResponseDto.builder().requestId(requestId).build();//나중에 암호화 적용해서 반환하게 변경
        ApiResponse<CommentaryResponseDto> apiResponse = new ApiResponse<>(true, "Video request created successfully", responseDto);
        return ResponseEntity.ok(apiResponse);
    }
}
