# log_middleware.py

import logging
from fastapi import Request


# HTTP 요청 로깅 미들웨어
def log_middleware(app, http_debug=False):
    logger = logging.getLogger("http_logger")
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)
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
