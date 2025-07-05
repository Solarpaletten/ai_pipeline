"""
Middleware для логирования запросов
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Логируем входящий запрос
        logger.info(f"Запрос: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Логируем время выполнения
        process_time = time.time() - start_time
        logger.info(f"Ответ: {response.status_code} за {process_time:.4f}с")
        
        return response
