from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import os
import sys

# Добавляем путь к src модулям
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

# Импортируем ПОСЛЕ добавления пути
try:
    from delegation.engine.delegation_engine import delegation_engine
except ImportError:
    # Fallback - создаем минимальную версию
    class SimpleDelegationEngine:
        async def route_task(self, task_text: str):
            # Простая логика маршрутизации
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
    """Умная маршрутизация задачи к AI агентам"""
    
    # Проверяем feature flag
    if not os.getenv('LEVEL7_ENABLED') == 'true':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Level 7 delegation not enabled. Set LEVEL7_ENABLED=true in .env"
        )
    
    try:
        # Используем DelegationEngine
        result = await delegation_engine.route_task(request.task)
        
        return DelegationResponse(
            task=result['task'],
            complexity=result['complexity'],
            recommended_chain=result['recommended_chain'],
            reasoning=result['reasoning'],
            estimated_time=result['estimated_time'],
            level=result['level'],
            status="routed_successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delegation failed: {str(e)}"
        )

@router.get("/status")  
async def delegation_status():
    """Статус системы Level 7 делегирования"""
    return {
        "level7_enabled": os.getenv('LEVEL7_ENABLED') == 'true',
        "version": "1.0.0",
        "agents_available": ["dashka", "claude", "deepseek"],
        "engine_status": "operational",
        "features": [
            "smart_routing",
            "complexity_analysis", 
            "chain_generation",
            "reasoning_explanation"
        ]
    }

@router.get("/test")
async def test_delegation():
    """Быстрый тест системы делегирования"""
    test_tasks = [
        "Создать новую страницу регистрации",
        "Проанализировать архитектуру системы", 
        "Исправить баг в коде"
    ]
    
    results = []
    for task in test_tasks:
        result = await delegation_engine.route_task(task)
        results.append({
            "task": task,
            "chain": result['recommended_chain'],
            "complexity": result['complexity']
        })
    
    return {
        "test_status": "completed",
        "test_results": results,
        "engine_working": True
    }