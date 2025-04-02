from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, Mount
from starlette.responses import Response
import uvicorn
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# MCP 서버 생성
mcp = FastMCP("구구단 선생님")

@mcp.tool()
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

def create_app():
    # SSE 설정
    sse = SseServerTransport("/sse")

    async def handle_sse(request):
        if request.method == "OPTIONS":
            return Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": "http://localhost:3000",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Credentials": "true",
                }
            )
            
        if request.method not in ["GET", "POST"]:
            return Response(
                status_code=405,
                headers={
                    "Access-Control-Allow-Origin": "http://localhost:3000",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Credentials": "true",
                }
            )

        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                mcp._mcp_server.create_initialization_options(),
            )

    # Starlette 앱 생성
    app = Starlette(debug=True)
    
    # CORS 미들웨어 추가
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # 라우트 설정
    app.add_route("/sse", handle_sse, methods=["GET", "POST", "OPTIONS"])
    app.mount("/messages", app=sse.handle_post_message)
    
    return app

app = create_app()

if __name__ == "__main__":
    log.info(f"FastMCP 서버 '{mcp.name}' 시작...")
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
