package com.wizard.api_server.common.response;

import lombok.Builder;
import lombok.Getter;

@Getter
public class ApiResponse<T> {
    private boolean  status;
    private String message;
    private T data;

    @Builder
    public ApiResponse(boolean status, String message, T data) {
        this.status = status;
        this.message = message;
        this.data = data;
    }
}
