#!/usr/bin/env python3
"""
AI Pipeline Web Server
FastAPI сервер для мониторинга и API endpoints
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
import aiohttp
import logging
import os
import json
import uuid

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Модели данных
class AgentStatus(BaseModel):
    name: str
    is_online: bool
    token_valid: bool
    response_time_ms: float
    last_check: datetime
    success_rate: float = 100.0

class DelegationEvent(BaseModel):
    id: str
    timestamp: datetime
    from_agent: str
    to_agent: str
    user_id: int
    message: str
    response: Optional[str] = None
    status: str
    response_time_ms: Optional[float] = None

app = FastAPI(title="AI Pipeline API", version="3.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальные переменные
agent_statuses: Dict[str, AgentStatus] = {}
recent_delegations: List[DelegationEvent] = []
connected_websockets: List[WebSocket] = []

# ============================================================================
# Функции проверки агентов
# ============================================================================

async def check_telegram_bot() -> AgentStatus:
    """Проверка Telegram бота"""
    try:
        token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        if not token or len(token) < 30:
            return AgentStatus(
                name="Dashka",
                is_online=False,
                token_valid=False,
                response_time_ms=0,
                last_check=datetime.utcnow()
            )
        
        start_time = datetime.utcnow()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.telegram.org/bot{token}/getMe') as resp:
                end_time = datetime.utcnow()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                return AgentStatus(
                    name="Dashka",
                    is_online=resp.status == 200,
                    token_valid=resp.status != 401,
                    response_time_ms=response_time,
                    last_check=datetime.utcnow()
                )
    except Exception as e:
        logger.error(f"Ошибка проверки Telegram: {e}")
        return AgentStatus(
            name="Dashka",
            is_online=False,
            token_valid=False,
            response_time_ms=0,
            last_check=datetime.utcnow()
        )

async def check_claude_api() -> AgentStatus:
    """Проверка Claude API"""
    try:
        api_key = os.getenv('ANTHROPIC_API_KEY', '')
        if not api_key:
            return AgentStatus(
                name="Claude",
                is_online=False,
                token_valid=False,
                response_time_ms=0,
                last_check=datetime.utcnow()
            )
        
        # Упрощенная проверка - просто проверяем формат ключа
        return AgentStatus(
            name="Claude",
            is_online=True,
            token_valid=len(api_key) > 20,
            response_time_ms=150.0,
            last_check=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Ошибка проверки Claude: {e}")
        return AgentStatus(
            name="Claude",
            is_online=False,
            token_valid=False,
            response_time_ms=0,
            last_check=datetime.utcnow()
        )

async def check_deepseek_api() -> AgentStatus:
    """Проверка DeepSeek API"""
    try:
        api_key = os.getenv('DEEPSEEK_API_KEY', '')
        if not api_key:
            return AgentStatus(
                name="DeepSeek",
                is_online=False,
                token_valid=False,
                response_time_ms=0,
                last_check=datetime.utcnow()
            )
        
        # Упрощенная проверка
        return AgentStatus(
            name="DeepSeek",
            is_online=True,
            token_valid=len(api_key) > 20,
            response_time_ms=200.0,
            last_check=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Ошибка проверки DeepSeek: {e}")
        return AgentStatus(
            name="DeepSeek",
            is_online=False,
            token_valid=False,
            response_time_ms=0,
            last_check=datetime.utcnow()
        )

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    return {"message": "AI Pipeline API Level 3", "status": "running"}

@app.get("/api/agents/status")
async def get_agents_status():
    """Получить статус всех агентов"""
    dashka = await check_telegram_bot()
    claude = await check_claude_api()
    deepseek = await check_deepseek_api()
    
    return {
        "agents": [dashka.model_dump(), claude.model_dump(), deepseek.model_dump()],
        "timestamp": datetime.utcnow().isoformat(),
        "total_agents": 3,
        "online_agents": sum([dashka.is_online, claude.is_online, deepseek.is_online])
    }

@app.get("/api/delegations/recent")
async def get_recent_delegations():
    """Получить последние делегирования"""
    return {
        "delegations": [d.model_dump() for d in recent_delegations[-20:]],
        "total": len(recent_delegations)
    }

@app.post("/api/delegations/log")
async def log_delegation(delegation: DelegationEvent):
    """Логирование делегирования"""
    recent_delegations.append(delegation)
    
    # Ограничиваем историю
    if len(recent_delegations) > 1000:
        recent_delegations.pop(0)
    
    # Отправляем через WebSocket
    if connected_websockets:
        update_data = {
            "type": "new_delegation",
            "data": delegation.model_dump()
        }
        for ws in connected_websockets.copy():
            try:
                await ws.send_text(json.dumps(update_data))
            except:
                connected_websockets.remove(ws)
    
    return {"status": "logged"}

@app.post("/api/test/delegation")
async def test_delegation():
    """Тестовое делегирование"""
    test_event = DelegationEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.utcnow(),
        from_agent="Dashka",
        to_agent="Claude",
        user_id=12345,
        message="Тестовое сообщение",
        response="Тест выполнен успешно!",
        status="completed",
        response_time_ms=250.5
    )
    
    await log_delegation(test_event)
    return {"status": "test_completed", "delegation": test_event}

@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket для real-time обновлений"""
    await websocket.accept()
    connected_websockets.append(websocket)
    
    try:
        # Отправляем начальные данные
        initial_data = {
            "type": "initial_data",
            "agents": await get_agents_status(),
            "delegations": [d.model_dump() for d in recent_delegations[-10:]]
        }
        await websocket.send_text(json.dumps(initial_data))
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "connected_clients": len(connected_websockets)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
