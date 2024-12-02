# log_middleware.py

import logging
from fastapi import Request

# 전역 로그 설정
def setup_logging(level=logging.INFO):
    """
    전역 로깅 설정
    :param level: 로깅 레벨 (기본값: logging.INFO)
    """
    logging.getLogger().setLevel(level)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)

# HTTP 요청 로깅 미들웨어
def log_middleware(app, logger, http_debug=False):
    @app.middleware("http")
    async def log_request(request: Request, call_next):
        if http_debug:  # http_debug가 True일 때만 로그를 출력
            try:
                body = await request.body()
                logger.info(f"Request body: {body.decode('utf-8', errors='replace')}")
            except UnicodeDecodeError as e:
                logger.error(f"Failed to decode request body: {e}")
            
            headers = dict(request.headers)
            logger.info(f"Request headers: {headers}")
        
        response = await call_next(request)
        return response
