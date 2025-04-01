FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# Git 설치 및 MCP SDK 설치
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir git+https://github.com/modelcontextprotocol/python-sdk.git@v1.6.0

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 서버 실행
CMD ["python", "src/server.py"]