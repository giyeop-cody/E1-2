# 1. 아규먼트 설정 (기본값: 3.10-slim-bookworm)
ARG PYTHON_VERSION=3.10-slim-bookworm
FROM python:${PYTHON_VERSION}

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 작업 디렉토리 설정
WORKDIR /app

# 2. pip 업데이트
RUN pip install --no-cache-dir --upgrade pip

# 3. [캐시 최적화] pyproject.toml만 먼저 복사
COPY pyproject.toml ./

# 4. 설치
# pyproject.toml에 정의된 내용을 바탕으로 설치를 진행합니다.
RUN pip install --no-cache-dir . 2>/dev/null || pip install --no-cache-dir setuptools

# 5. 나머지 소스 파일(*.py) 복사
COPY *.py ./

# 6. 실행 명령
CMD ["python", "main.py"]