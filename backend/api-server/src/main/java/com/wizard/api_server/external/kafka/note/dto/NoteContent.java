package com.wizard.api_server.external.kafka.note.dto;

public record NoteContent(
        String videoId,
        long startTime,
        String content) {
}
