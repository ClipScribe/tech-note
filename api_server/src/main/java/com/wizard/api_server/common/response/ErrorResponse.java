package com.wizard.api_server.common.response;

import lombok.Getter;

@Getter
public class ErrorResponse {

    private String message;
    private String code;

    public ErrorResponse(String message, String code) {
        this.message = message;
        this.code = code;
    }
}
