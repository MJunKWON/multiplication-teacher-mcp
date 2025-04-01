# 구구단 선생님 MCP 서버

구구단을 가르치는 MCP 서버입니다. Claude가 직접 호출할 수 있는 도구를 제공합니다.

## 기능

* 1단부터 9단까지의 구구단 계산
* MCP 도구를 통한 자동 호출
* Docker 컨테이너 지원

## 설치 및 실행

### 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt
pip install git+https://github.com/modelcontextprotocol/python-sdk.git

# 서버 실행
python src/server.py
```

### Docker 실행

```bash
# 이미지 빌드
docker build -t multiplication-teacher .

# 컨테이너 실행
docker run -p 8000:8000 multiplication-teacher
```

## 사용 예시

1. "7단을 알려주세요"
2. "구구단 중에서 3단이 궁금해요"
3. "9단을 보여주세요"

## 주의사항

* 1부터 9까지의 숫자만 입력 가능합니다.
* 다른 숫자를 입력하면 오류 메시지가 반환됩니다.