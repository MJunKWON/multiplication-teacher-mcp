import os
import anthropic
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# Anthropic 클라이언트 초기화
client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

def test_multiplication():
    # Claude에게 구구단 요청
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="You are a helpful assistant that teaches multiplication tables.",
        messages=[
            {
                "role": "user",
                "content": "7단 구구단을 알려줘"
            }
        ]
    )
    
    # 응답 출력
    print("Claude의 응답:")
    print(message.content)

if __name__ == "__main__":
    test_multiplication()