package com.wizard.api_server.repository;

import com.wizard.api_server.domain.CommentaryLevel;
import com.wizard.api_server.domain.entity.Commentary;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.UUID;

public interface CommentaryRepository extends JpaRepository<Commentary, Long> {

    // JPQL을 사용하여 CommentaryRequest의 requestId(UUID)를 기준으로 Commentary 조회
    @Query("SELECT c FROM Commentary c WHERE c.commentaryRequest.requestId = :requestId AND c.level = :level")
    List<Commentary> findByCommentaryRequestRequestIdAndLevel(@Param("requestId") UUID requestId, @Param("level") CommentaryLevel level);
}
