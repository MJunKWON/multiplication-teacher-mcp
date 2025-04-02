from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

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

# Starlette 앱에 SSE 엔드포인트 마운트
starlette_app = Starlette(
    routes=[
        Mount("/", app=app.sse_app()),
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000)