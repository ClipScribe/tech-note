# 기술 스택

### Backend

- SpringBoot
- FastAPI
- Wisper

### Frontend

- Nuxt3
- Pinia
- Quasar

# 프로젝트 구조

```bash
backend/
├── kafka
├── api-server # SpringBoot
├── llm-server # FastAPI
└── stt-server # FastAPI
frontend/   # Nuxt3
```

# 애플리케이션 실행

### Frontend

```bash
npm i
npm run dev
```

### Backend

```bash
# api-server
./gradlew build
./gradlew bootRun

# llm-server, stt-server
python3 -m venv venv
source vnev/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

uvicorn app.main:app --reload
```
