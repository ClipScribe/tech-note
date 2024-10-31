package com.wizard.api_server.domain.entity;

import com.wizard.api_server.domain.CommentaryLevel;
import jakarta.persistence.*;

import java.time.Instant;

@Entity
@Table(name = "commentories")
public class Commentary {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", updatable = false, nullable = false)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "commentary_request_id", nullable = false)
    private CommentaryRequest commentaryRequest;

    @Lob
    @Column(name = "content", nullable = false)
    private String content;

    @Enumerated(EnumType.STRING)
    @Column(name = "level", nullable = false)
    private CommentaryLevel level;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    // Getters and Setters

    @PrePersist
    protected void onCreate() {
        createdAt = Instant.now();
    }

    // Constructors, equals, hashCode, toString methods
}
