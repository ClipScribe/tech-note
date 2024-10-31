package com.wizard.api_server.common.exception.customexceptions;

import com.wizard.api_server.common.exception.CustomException;
import com.wizard.api_server.common.exception.ErrorCode;

public class CommentaryRequestCreationException extends CustomException {

    public CommentaryRequestCreationException() {
        super(ErrorCode.COMMENTARY_REQUEST_CREATION_FAILED);
    }

    public CommentaryRequestCreationException(String message, Throwable cause) {
        super(ErrorCode.COMMENTARY_REQUEST_CREATION_FAILED, cause);
    }
}
