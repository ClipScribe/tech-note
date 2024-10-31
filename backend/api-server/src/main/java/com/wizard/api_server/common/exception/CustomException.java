package com.wizard.api_server.common.exception;


import lombok.Getter;
import lombok.RequiredArgsConstructor;


@Getter
public class CustomException extends RuntimeException {

    private final ErrorCode errorCode;

    // ErrorCode만 받는 생성자
    public CustomException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }

    // ErrorCode와 Throwable을 받는 생성자
    public CustomException(ErrorCode errorCode, Throwable cause) {
        super(errorCode.getMessage(), cause);
        this.errorCode = errorCode;
    }

    // ErrorCode와 커스텀 메시지, Throwable을 받는 생성자
    public CustomException(ErrorCode errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }

}
