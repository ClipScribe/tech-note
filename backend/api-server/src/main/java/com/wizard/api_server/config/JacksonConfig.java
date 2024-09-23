package com.wizard.api_server.config;

//@Configuration
//public class JacksonConfig {
//
//    /**
//     * Jackson 라이브러리는 LocalDateTime을 기본적으로 배열 형식으로 직렬화한다.
//     * "timestamp":[2024,11,5,4,10,49,171439000]
//     *
//     * 따라서 ISO 8601 형식(ex: 2024-11-05T04:10:49.121197)으로 직렬화되도록 설정한다.
//     */
//    @Bean
//    public ObjectMapper objectMapper() {
//        ObjectMapper mapper = new ObjectMapper();
//        mapper.registerModule(new JavaTimeModule());
//        mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
//        return mapper;
//    }
//}

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;

@Configuration
public class JacksonConfig {

    @Bean
    public ObjectMapper objectMapper(Jackson2ObjectMapperBuilder builder) {
        return builder
                .featuresToDisable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                .modules(new JavaTimeModule())
                .build();
    }
}