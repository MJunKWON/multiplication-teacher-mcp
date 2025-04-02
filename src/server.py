import os
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 앱 생성
api = FastAPI()

# CORS 설정
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP 서버 생성
app = FastMCP("구구단 선생님")

@app.tool()
def multiply(number: int) -> str:
    """구구단을 계산합니다.
    
    Args:
        number: 1-9 사이의 숫자
        
    Returns:
        구구단 결과
    """
    if not 1 <= number <= 9:
        return "1부터 9까지의 숫자만 입력해주세요."
    
    return "\n".join([f"{number} x {i} = {number * i}" for i in range(1, 10)])

if __name__ == "__main__":
    # Railway에서 제공하는 PORT 환경변수 사용
    port = int(os.getenv("PORT", "3000"))
    # SSE 전송 방식으로 실행
    app.run(transport="sse", host="0.0.0.0", port=port)