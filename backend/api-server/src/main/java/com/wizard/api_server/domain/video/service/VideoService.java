package com.wizard.api_server.domain.video.service;

import com.wizard.api_server.domain.video.event.SendVideoLinkEvent;
import com.wizard.api_server.external.kafka.producer.VideoLinkProducer;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class VideoService {
    private final VideoLinkProducer videoLinkProducer;

    public void sendVideoLink(String videoLink) {
        SendVideoLinkEvent event = new SendVideoLinkEvent(videoLink);
        videoLinkProducer.publish(event);
    }
}
