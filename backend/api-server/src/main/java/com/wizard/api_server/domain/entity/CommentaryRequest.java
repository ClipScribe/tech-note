package com.wizard.api_server.domain.entity;

import com.wizard.api_server.domain.RequestStatus;

import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.UuidGenerator;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Getter
@Entity
@Table(name = "commentary_requests", indexes = {
        @Index(name = "idx_request_id", columnList = "request_id", unique = true)
})
public class CommentaryRequest {

    @Id
    @GeneratedValue
    @Column(name = "id", updatable = false, nullable = false)
    private Long id;

    @Column(name = "request_id", updatable = false, nullable = false, unique = true)
    @UuidGenerator
    private UUID requestId;

    @Column(name = "youtube_link", nullable = false)
    private String youtubeLink;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private RequestStatus status;

    @Column(name = "progress", nullable = false)
    private Integer progress;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @OneToMany(mappedBy = "commentaryRequest", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Commentary> commentaries;

    // Getters and Setters

    @PrePersist
    protected void onCreate() {
        createdAt = Instant.now();
        updatedAt = Instant.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = Instant.now();
    }

    // Constructors, equals, hashCode, toString methods
}
