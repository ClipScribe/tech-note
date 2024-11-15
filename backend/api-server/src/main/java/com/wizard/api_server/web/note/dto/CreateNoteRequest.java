package com.wizard.api_server.web.note.dto;

public record CreateNoteRequest (
        String videoId,
        String userLevel
) {
}
