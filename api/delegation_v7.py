"""
Level 7: Delegation API v1.0
REST API для умной маршрутизации задач
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import os
import sys

sys.path.append('/app/src')
router = APIRouter(tags=["Level 7 Delegation"])

class DelegationRequest(BaseModel):
    task: str
    user_id: str = "default"

class DelegationResponse(BaseModel):
    task: str
    complexity: str
    recommended_chain: list
    reasoning: str
    estimated_time: int
    level: int
    status: str

class SimpleDelegationEngine:
    async def route_task(self, task_text: str):
        if "баг" in task_text.lower() or "исправить" in task_text.lower():
            return {
                'task': task_text,
                'complexity': 'MEDIUM',
                'recommended_chain': ['claude', 'deepseek'],
                'reasoning': 'Анализ проблемы + техническая реализация',
                'estimated_time': 10,
                'level': 7
            }
        elif "анализ" in task_text.lower() or "архитектуру" in task_text.lower():
            return {
                'task': task_text,
                'complexity': 'MEDIUM',
                'recommended_chain': ['claude', 'deepseek'],
                'reasoning': 'Аналитическое планирование + техническая проработка',
                'estimated_time': 15,
                'level': 7
            }
        elif "создать" in task_text.lower() and "систему" in task_text.lower():
            return {
                'task': task_text,
                'complexity': 'COMPLEX',
                'recommended_chain': ['dashka', 'claude', 'deepseek', 'dashka'],
                'reasoning': 'Комплексная задача - полный цикл делегирования',
                'estimated_time': 20,
                'level': 7
            }
        else:
            return {
                'task': task_text,
                'complexity': 'SIMPLE',
                'recommended_chain': ['deepseek'],
                'reasoning': 'Простая задача - прямая реализация',
                'estimated_time': 5,
                'level': 7
            }

delegation_engine = SimpleDelegationEngine()

@router.post("/route", response_model=DelegationResponse)
async def route_task(request: DelegationRequest):
    if not os.getenv('LEVEL7_ENABLED') == 'true':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level 7 not enabled")
    
    result = await delegation_engine.route_task(request.task)
    return DelegationResponse(**result, status="routed_successfully")

@router.get("/status")  
async def delegation_status():
    return {
        "level7_enabled": os.getenv('LEVEL7_ENABLED') == 'true',
        "version": "1.0.0",
        "agents_available": ["dashka", "claude", "deepseek"],
        "engine_status": "operational"
    }

@router.get("/test")
async def test_delegation():
    test_tasks = ["Создать страницу", "Проанализировать систему", "Исправить баг"]
    results = []
    for task in test_tasks:
        result = await delegation_engine.route_task(task)
        results.append({"task": task, "chain": result['recommended_chain'], "complexity": result['complexity']})
    return {"test_status": "completed", "test_results": results, "engine_working": True}
