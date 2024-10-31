package com.wizard.api_server.kafka.commentarylistener;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;

import java.util.HashMap;
import java.util.Map;

/**
 * Kafka 소비자 설정 클래스
 * 'transcription_results' 토픽을 소비하기 위한 설정을 정의합니다.
 */
@EnableKafka
@Configuration
public class KafkaCommentaryResultConsumerConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${spring.kafka.consumer.group-id}")
    private String groupId;

    /**
     * Kafka 소비자 팩토리 빈 생성
     *
     * @return ConsumerFactory<String, String>
     */
    @Bean
    public ConsumerFactory<String, String> commentaryConsumerFactory() {
        Map<String, Object> props = new HashMap<>();

        // Kafka 브로커 주소 설정
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);

        // 소비자 그룹 ID 설정
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);

        // 키 및 값 디시리얼라이저 설정
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);

        // 오프셋 자동 초기화 설정
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        return new DefaultKafkaConsumerFactory<>(props);
    }

    /**
     * Kafka 리스너 컨테이너 팩토리 빈 생성
     *
     * @return ConcurrentKafkaListenerContainerFactory<String, String>
     */
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaCommentaryListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, String> factory
                = new ConcurrentKafkaListenerContainerFactory<>();

        factory.setConsumerFactory(commentaryConsumerFactory());

        return factory;
    }
}