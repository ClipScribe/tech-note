package com.wizard.api_server.common.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    //400
    UNKNOWN("000_UNKNOWN", "알 수 없는 에러가 발생했습니다."),
    INVALID_REQUESTID("001_INVALID_REQUESTID", "유효하지 않는 requestId입니다."),
    //500
    COMMENTARY_REQUEST_CREATION_FAILED("000_COMMENTARY_REQUEST_CREATION_FAILED", "CommentaryRequest를 생성하는데 실패했습니다.");

    private final String code;
    private final String message;


}
