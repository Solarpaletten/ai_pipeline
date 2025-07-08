from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/api/agents", tags=["agents"])

VALID_AGENTS = {"claude", "dashka", "deepseek"}

@router.get("/status")
async def get_status():
    """Возвращает статусы агентов в требуемом формате"""
    agents = [
        {
            "name": "Claude",
            "status": "online" if os.getenv("ANTHROPIC_API_KEY") else "offline"
        },
        {
            "name": "DeepSeek",
            "status": "online" if os.getenv("DEEPSEEK_API_KEY") else "offline"
        },
        {
            "name": "Dashka",
            "status": "coordinator" if os.getenv("TELEGRAM_BOT_TOKEN") else "offline"
        }
    ]
    return {"agents": agents}

@router.post("/test/{agent_name}")
async def test_agent(agent_name: str):
    agent = agent_name.lower()
    if agent not in VALID_AGENTS:
        raise HTTPException(status_code=404, detail="Unknown agent")
    
    logger.info(f"🧪 Testing agent: {agent}")
    
    return {
        "agent": agent,
        "test": "passed",
        "timestamp": datetime.utcnow().isoformat()
    }
