package com.wizard.api_server.mapper;

import com.wizard.api_server.controller.dto.CommentaryRequestDto;
import com.wizard.api_server.controller.dto.CommentaryResponseDto;
import com.wizard.api_server.domain.entity.CommentaryRequest;
import com.wizard.api_server.kafka.requestproducer.message.CommentaryRequestMessage;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

/**
 * CommentaryRequest와 CommentaryRequestDto 간의 매핑을 담당하는 매퍼 인터페이스
 */
@Mapper()
public interface CommentaryRequestMapper {

    CommentaryRequestMapper INSTANCE = Mappers.getMapper(CommentaryRequestMapper.class);

    /**
     * CommentaryRequestDto를 CommentaryRequest 엔티티로 매핑
     *
     * @param dto 데이터 전송 객체
     * @return 엔티티 객체
     */

    CommentaryRequest toEntity(CommentaryRequestDto dto);

    /**
     * CommentaryRequest 엔티티를 CommentaryRequestDto로 매핑
     *
     * @param entity 엔티티 객체
     * @return 데이터 전송 객체
     */
    CommentaryResponseDto toDto(CommentaryRequest entity);

    CommentaryRequestMessage toMessageDto(CommentaryRequest entity);
}
