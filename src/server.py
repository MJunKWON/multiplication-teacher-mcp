from mcp.server.fastmcp import FastMCP
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# MCP 서버 생성 (명시적 경로 설정)
app = FastMCP(
    name="구구단 선생님",
    sse_path="/messages/",  # SSE 연결용 GET 엔드포인트
    message_path="/messages/",  # 메시지 전송용 POST 엔드포인트
    log_level="INFO"
)

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
    log.info(f"FastMCP 서버 '{app.name}' 시작...")
    log.info(f"SSE GET 엔드포인트: {app.settings.sse_path}")
    log.info(f"메시지 POST 엔드포인트: {app.settings.message_path}")
    
    try:
        # SSE 전송 방식으로 서버 실행
        app.run(transport="sse")
    except Exception as e:
        log.exception("서버 실행 중 오류 발생")
    finally:
        log.info("서버 종료")