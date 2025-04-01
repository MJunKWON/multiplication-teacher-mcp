from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools.base import Tool
from pydantic import BaseModel
import os
from typing import List

app = FastMCP(
    name="구구단 선생님",
    description="구구단을 가르쳐주는 MCP 서버입니다",
    version="1.0.0"
)

class MultiplicationInput(BaseModel):
    number: int

@app.tool()
def multiplication_table(number: int) -> str:
    """주어진 숫자의 구구단을 계산합니다 (1-9)
    
    Args:
        number: 구구단을 계산할 숫자 (1-9)
        
    Returns:
        str: 구구단 결과
    """
    if not 1 <= number <= 9:
        return "1부터 9까지의 숫자만 입력 가능합니다."
    
    result = [f"{number} x {i} = {number * i}" for i in range(1, 10)]
    return "\n".join(result)

if __name__ == "__main__":
    app.run()