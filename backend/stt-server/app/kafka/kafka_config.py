# app/kafka/kafka_config.py

# Kafka 서버 주소 (IP:포트 형식으로 작성)
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # 예: 로컬 호스트에 설치된 Kafka 브로커

#topic
VIDEO_REQUEST_TOPIC = "video_request_topic"
STT_RESULT_TOPIC = "stt_result_topic"

# 메시지의 전송에 대한 확인 수준
# all: 모든 복제본이 메시지를 확인해야 성공으로 간주
# 1: 리더 복제본이 메시지를 확인하면 성공으로 간주
# 0: 메시지 전송만 하고 확인을 기다리지 않음
ACKS = "all"

# 한 번에 전송할 수 있는 최대 메시지 크기 (바이트 단위)
MAX_BATCH_SIZE = 16384  # 예: 16KB

# 메시지를 모으기 위한 최대 지연 시간 (밀리초)
LINGER_MS = 10  # 예: 10ms

# 재시도 간의 백오프 시간 (밀리초)
RETRY_BACKOFF_MS = 100  # 예: 100ms