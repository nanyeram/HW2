# 베이스 이미지 (가볍고 안정적인 3.11-slim 사용)
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 구성 업데이트 및 오디오 처리(librosa, sounddevice)를 위한 OS 레벨 의존성 패키지 설치
# 레이어 캐싱 최적화 및 이미지 용량 감축을 위해 rm -rf 명령어 포함
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    portaudio19-dev \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 의존성 파일 복사 및 설치 (코드가 변경되어도 패키지를 매번 다시 다운받지 않도록 캐시 레이어 분리 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스코드 및 모델 가중치 파일 전체 복사
COPY . .

# 컨테이너가 8000번 포트를 사용함을 명시
EXPOSE 8000

# 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
