from mcp.server.fastmcp import FastMCP, Tool
from pydantic import BaseModel
import os
from typing import List

app = FastMCP("구구단 선생님")

class MultiplicationInput(BaseModel):
    number: int

@Tool(description="주어진 숫자의 구구단을 계산합니다 (1-9)")
def multiplication_table(input: MultiplicationInput) -> List[str]:
    number = input.number
    if not 1 <= number <= 9:
        raise ValueError("숫자는 1에서 9 사이여야 합니다")
    
    results = []
    for i in range(1, 10):
        result = f"{number} x {i} = {number * i}"
        results.append(result)
    
    return results

if __name__ == "__main__":
    app.run()