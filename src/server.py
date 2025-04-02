from mcp.server.fastmcp import FastMCP

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
    # SSE 전송 방식으로만 실행
    app.run(transport="sse")