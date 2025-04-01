from mcp.server.fastmcp import FastMCP

# Create an MCP server
app = FastMCP(
    name="구구단 선생님",
    description="구구단을 가르쳐주는 MCP 서버입니다",
    version="1.0.0"
)

@app.tool()
def multiplication_table(number: int) -> str:
    """주어진 숫자의 구구단을 계산합니다 (1-9)"""
    if not 1 <= number <= 9:
        return "1부터 9까지의 숫자만 입력해주세요."
    
    result = []
    for i in range(1, 10):
        result.append(f"{number} x {i} = {number * i}")
    return "\n".join(result)

if __name__ == "__main__":
    app.run()