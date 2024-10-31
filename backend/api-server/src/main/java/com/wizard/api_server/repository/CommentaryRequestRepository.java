package com.wizard.api_server.repository;

import com.wizard.api_server.domain.entity.CommentaryRequest;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

public interface CommentaryRequestRepository extends JpaRepository<CommentaryRequest, Long> {
    Optional<CommentaryRequest> findByRequestId(UUID requestId);
}
