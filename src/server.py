from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, Mount
from starlette.responses import Response, JSONResponse
import uvicorn
import logging
import json
from uuid import UUID

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
        return {
            "status": "error",
            "message": "1부터 9까지의 숫자만 입력해주세요."
        }
    
    result = "\n".join([f"{number} x {i} = {number * i}" for i in range(1, 10)])
    return {
        "status": "success",
        "message": result
    }

def create_app():
    # SSE 설정
    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        # CORS 헤더
        cors_headers = {
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Credentials": "true",
        }

        # OPTIONS 요청 처리
        if request.method == "OPTIONS":
            return Response(status_code=200, headers=cors_headers)

        # GET 요청 처리 (SSE 연결)
        if request.method == "GET":
            cors_headers.update({
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            })
            
            try:
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
            except Exception as e:
                log.error(f"SSE 연결 에러: {str(e)}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "status": "error",
                        "message": f"SSE 연결 에러: {str(e)}"
                    },
                    headers=cors_headers
                )

        return Response(status_code=405, headers=cors_headers)

    async def handle_messages(request):
        # CORS 헤더
        cors_headers = {
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Credentials": "true",
        }

        # OPTIONS 요청 처리
        if request.method == "OPTIONS":
            return Response(status_code=200, headers=cors_headers)

        # POST 요청 처리
        if request.method == "POST":
            try:
                # session_id 확인
                session_id_param = request.query_params.get("session_id")
                if not session_id_param:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "status": "error",
                            "message": "session_id가 필요합니다."
                        },
                        headers=cors_headers
                    )

                try:
                    session_id = UUID(session_id_param)
                except ValueError:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "status": "error",
                            "message": "잘못된 session_id 형식입니다."
                        },
                        headers=cors_headers
                    )

                # 메시지 본문 확인
                body = await request.json()
                message = body.get("message")
                if not message:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "status": "error",
                            "message": "메시지가 없습니다. 'message' 필드가 필요합니다."
                        },
                        headers=cors_headers
                    )

                # 메시지 처리
                log.info(f"세션 ID {session_id_param}로부터 메시지 수신: {message}")
                
                # URL에 세션 ID를 포함시켜 scope를 수정합니다
                modified_scope = request.scope.copy()
                modified_scope["query_string"] = f"session_id={session_id_param}".encode()
                
                try:
                    # 메시지를 MCP 서버에 전달
                    await sse.handle_post_message(
                        scope=modified_scope,
                        receive=request.receive,
                        send=request._send
                    )
                    log.info("메시지가 MCP 서버에 전달되었습니다.")
                    
                    return JSONResponse(
                        status_code=202,
                        content={
                            "status": "success",
                            "message": "메시지가 전송되었습니다."
                        },
                        headers=cors_headers
                    )
                except Exception as e:
                    log.error(f"MCP 메시지 전달 실패: {str(e)}")
                    return JSONResponse(
                        status_code=500,
                        content={
                            "status": "error",
                            "message": f"MCP 메시지 전달 실패: {str(e)}"
                        },
                        headers=cors_headers
                    )
            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "message": "잘못된 JSON 형식입니다. Content-Type이 application/json인지 확인해주세요."
                    },
                    headers=cors_headers
                )
            except Exception as e:
                log.error(f"메시지 처리 에러: {str(e)}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "status": "error",
                        "message": f"메시지 처리 에러: {str(e)}"
                    },
                    headers=cors_headers
                )

        return Response(status_code=405, headers=cors_headers)

    # Starlette 앱 생성
    app = Starlette(debug=True)
    
    # CORS 미들웨어 추가
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:3002",
            "http://localhost:3003",
            "http://localhost:3004",
            "http://192.168.219.231:3000"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    # 라우트 설정
    app.add_route("/sse", handle_sse, methods=["GET", "OPTIONS"])
    app.add_route("/messages", handle_messages, methods=["POST", "OPTIONS"])
    
    return app

app = create_app()

if __name__ == "__main__":
    log.info(f"FastMCP 서버 '{mcp.name}' 시작...")
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
