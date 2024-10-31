package com.wizard.api_server.controller.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import lombok.Builder;
import lombok.Getter;

@Getter
public class CommentaryRequestDto {
    @NotBlank
    @Pattern(regexp = "https?://www\\.youtube\\.com/watch\\?v=.+", message = "유효한 YouTube 링크를 입력하세요.")
    private String youtubeLink;

    @Builder
    public CommentaryRequestDto(String videoLink) {
        this.youtubeLink = videoLink;
    }
}
