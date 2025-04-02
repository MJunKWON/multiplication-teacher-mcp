# 구구단 선생님 MCP

구구단을 계산해주는 MCP 서버입니다.

## 기능

- 1-9단까지의 구구단을 계산할 수 있습니다.
- Claude Desktop과 연동하여 사용할 수 있습니다.

## 설치 방법

1. Python 3.12 이상이 필요합니다.
2. 가상환경을 생성하고 활성화합니다:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
```

3. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

## 사용 방법

1. 서버 실행:
```bash
python src/server.py
```

2. Claude Desktop 설정:
```json
{
  "mcpServers": {
    "구구단": {
      "command": "python",
      "args": ["src/server.py"]
    }
  }
}
```

3. Claude Desktop에서 다음과 같이 사용할 수 있습니다:
   - "7단 구구단을 알려줘"
   - "3단을 계산해줘"

## Docker 사용

```bash
docker build -t multiplication-teacher .
docker run -p 8000:8000 multiplication-teacher
```