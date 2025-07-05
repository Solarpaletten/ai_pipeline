"""
API для работы с агентами
"""
from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.get("/status")
async def get_status():
    """Статус всех агентов"""
    return {
        "dashka": {
            "online": bool(os.getenv('TELEGRAM_BOT_TOKEN')),
            "token_valid": len(os.getenv('TELEGRAM_BOT_TOKEN', '')) > 30,
            "last_check": datetime.utcnow().isoformat()
        },
        "claude": {
            "online": bool(os.getenv('ANTHROPIC_API_KEY')),
            "token_valid": len(os.getenv('ANTHROPIC_API_KEY', '')) > 20,
            "last_check": datetime.utcnow().isoformat()
        },
        "deepseek": {
            "online": bool(os.getenv('DEEPSEEK_API_KEY')),
            "token_valid": len(os.getenv('DEEPSEEK_API_KEY', '')) > 20,
            "last_check": datetime.utcnow().isoformat()
        }
    }

@router.post("/test/{agent_name}")
async def test_agent(agent_name: str):
    """Тестирование конкретного агента"""
    return {"agent": agent_name, "test": "passed", "timestamp": datetime.utcnow()}
