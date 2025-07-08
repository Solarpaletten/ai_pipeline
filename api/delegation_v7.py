# api/delegation_v7.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class DelegationRequest(BaseModel):
    task: str
    user_id: str = "default"

@router.post("/route")
async def route_task(request: DelegationRequest):
    """Маршрутизация задачи к агентам"""
    
    # Проверяем feature flag
    if not os.getenv('LEVEL7_ENABLED') == 'true':
        raise HTTPException(404, "Level 7 delegation not enabled")
    
    # Простейшая реализация
    from src.delegation.engine.delegation_engine import DelegationEngine
    engine = DelegationEngine()
    
    chain = await engine.route_task(request.task)
    
    return {
        "task": request.task,
        "recommended_chain": chain,
        "status": "routed",
        "level": 7
    }

@router.get("/status")  
async def delegation_status():
    """Статус системы делегирования"""
    return {
        "level7_enabled": os.getenv('LEVEL7_ENABLED') == 'true',
        "version": "1.0.0",
        "agents_available": ["dashka", "claude", "deepseek"]
    }