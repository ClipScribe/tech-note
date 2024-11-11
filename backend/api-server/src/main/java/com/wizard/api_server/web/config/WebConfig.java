package com.wizard.api_server.web.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:3000")
                .allowedMethods("GET", "OPTIONS")
                .allowedHeaders("*")
                .allowedHeaders(
                "Content-Type",
                "X-Requested-With",// AJAX 요청 식별용
                "Accept",          // 서버 응답 타입 지정
                "Cache-Control"    // 캐싱 방지
        );
    }
}