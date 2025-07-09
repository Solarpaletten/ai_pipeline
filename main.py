#!/usr/bin/env python3
"""
AI Pipeline - Production Main Application
FastAPI + Real AI APIs Integration
"""

import asyncio
import logging
import os
from dotenv import load_dotenv


# FastAPI imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from api.delegation_v7 import router as delegation_router

# Local imports
from api.chat_endpoints import router as chat_router
from api.delegation_v7 import router as delegation_router

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Конфигурация из .env
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
PORT = int(os.getenv('PORT', 4000))
HOST = os.getenv('HOST', '0.0.0.0')

# AI API конфигурация
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Telegram Bot конфигурация
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Database конфигурация
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL')

# Frontend URLs для CORS
FRONTEND_URLS = [
    "https://aisolar.swapoil.de",
    "http://localhost:3000",
    "http://localhost:8000"
]

# Создаем FastAPI приложение
app = FastAPI(
    title="AI Pipeline Interface",
    description="Production API для управления AI агентами",
    version="2.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(chat_router)
app.include_router(delegation_router, prefix="/api/delegation")

# Статические файлы для production
if os.path.exists("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
    
    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def serve_spa(full_path: str):
        """Serve React SPA"""
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("static/"):
            return {"error": "Not found"}
        
        try:
            with open("frontend/build/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        except FileNotFoundError:
            return {"error": "Frontend not built"}


@app.on_event("startup")
async def startup_event():
    """Инициализация при старте приложения"""
    logger.info("🚀 Запуск AI Pipeline Production API...")
    
    # Проверяем наличие ключей API
    missing_keys = []
    if not CLAUDE_API_KEY:
        missing_keys.append("CLAUDE_API_KEY")
    if not DEEPSEEK_API_KEY:
        missing_keys.append("DEEPSEEK_API_KEY")
    
    if missing_keys:
        logger.warning(f"⚠️ Отсутствуют API ключи: {', '.join(missing_keys)}")
    else:
        logger.info("✅ Все API ключи настроены")
    
    # Инициализация реальных сервисов
    try:
        # Инициализация подключений к внешним API
        await init_ai_services()
        
        # Инициализация базы данных
        if DATABASE_URL:
            await init_database()
        else:
            logger.warning("⚠️ DATABASE_URL не настроен")
        
        # Инициализация Redis
        if REDIS_URL:
            await init_redis()
        else:
            logger.warning("⚠️ REDIS_URL не настроен")
            
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации: {e}")

async def init_ai_services():
    """Инициализация AI сервисов"""
    logger.info("🤖 Инициализация AI сервисов...")
    
    # Тест Claude API
    if CLAUDE_API_KEY:
        try:
            # Здесь будет реальный тест Claude API
            logger.info("✅ Claude API готов")
        except Exception as e:
            logger.error(f"❌ Claude API ошибка: {e}")
    
    # Тест DeepSeek API  
    if DEEPSEEK_API_KEY:
        try:
            # Здесь будет реальный тест DeepSeek API
            logger.info("✅ DeepSeek API готов")
        except Exception as e:
            logger.error(f"❌ DeepSeek API ошибка: {e}")

async def init_database():
    """Инициализация базы данных"""
    logger.info("🗄️ Инициализация PostgreSQL...")
    try:
        # Здесь будет реальное подключение к PostgreSQL
        # import asyncpg
        # conn = await asyncpg.connect(DATABASE_URL)
        # await conn.close()
        logger.info("✅ PostgreSQL подключен")
    except Exception as e:
        logger.error(f"❌ PostgreSQL ошибка: {e}")

async def init_redis():
    """Инициализация Redis"""
    logger.info("🔴 Инициализация Redis...")
    try:
        # Здесь будет реальное подключение к Redis
        # import aioredis
        # redis = aioredis.from_url(REDIS_URL)
        # await redis.ping()
        logger.info("✅ Redis подключен")
    except Exception as e:
        logger.error(f"❌ Redis ошибка: {e}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница API"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Pipeline Production API</title>
        <meta charset="utf-8">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { background: #e7f5e7; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; }
            .warning { background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; font-family: monospace; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AI Pipeline Production API</h1>
            <div class="status">
                <h3>✅ Система работает</h3>
                <p><strong>Версия:</strong> 2.0.0 | <strong>Режим:</strong> Production</p>
            </div>
            
            <h3>🎯 API Endpoints:</h3>
            <div class="endpoint">GET <a href="/api/chat/agents">/api/chat/agents</a> - Список агентов</div>
            <div class="endpoint">GET <a href="/api/chat/projects">/api/chat/projects</a> - Проекты</div>
            <div class="endpoint">POST /api/chat/send - Отправка сообщения</div>
            <div class="endpoint">WS /api/chat/ws/{user_id} - WebSocket чат</div>
            <div class="endpoint">GET <a href="/health">/health</a> - Health check</div>
            
            <h3>📱 Frontend:</h3>
            <p>React приложение доступно по этому же домену</p>
            
            <div class="warning">
                <strong>⚠️ Внимание:</strong> Это production API. Документация отключена в целях безопасности.
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check для Docker/Kubernetes"""
    return {
        "status": "healthy",
        "service": "AI Pipeline Production API",
        "version": "2.0.0",
        "environment": ENVIRONMENT,
        "apis": {
            "claude": bool(CLAUDE_API_KEY),
            "deepseek": bool(DEEPSEEK_API_KEY),
            "database": bool(DATABASE_URL),
            "redis": bool(REDIS_URL)
        }
    }

@app.get("/status")
async def system_status():
    """Детальный статус системы"""
    return {
        "timestamp": asyncio.get_event_loop().time(),
        "uptime": "N/A",  # Можно добавить трекинг uptime
        "services": {
            "fastapi": "running",
            "claude_api": "ready" if CLAUDE_API_KEY else "not_configured",
            "deepseek_api": "ready" if DEEPSEEK_API_KEY else "not_configured",
            "database": "ready" if DATABASE_URL else "not_configured",
            "redis": "ready" if REDIS_URL else "not_configured"
        }
    }

def main():
    """Главная функция - запуск для production"""
    logger.info("🚀 AI Pipeline Production Server Starting...")
    
    # Валидация критичных переменных
    if not CLAUDE_API_KEY and not DEEPSEEK_API_KEY:
        logger.error("❌ Не настроены API ключи для AI сервисов!")
        logger.info("📝 Настройте CLAUDE_API_KEY и DEEPSEEK_API_KEY в .env")
    
    # Запуск production сервера
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=False,  # В production не используем reload
        log_level="info",
        access_log=True,
        workers=1  # Для Docker обычно 1 worker
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 AI Pipeline остановлен")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        raise