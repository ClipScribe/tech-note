# ApiServer

## ApiServer to STTServer

스크립트를 이용해 curl 요청
```bash
chmod +x http.sh
./http.sh
```

![](../../docs/image/api_request.png)


topic 에 produce 한 메시지 확인

```bash
docker exec -it kafka /bin/bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic video-event --from-beginning
```

![](../../docs/image/api_to_stt.png)