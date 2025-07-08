# src/delegation/engine/delegation_engine.py
from typing import Dict, List, Optional
from enum import Enum
import asyncio

class TaskComplexity(Enum):
    SIMPLE = 1      # Один агент
    MEDIUM = 2      # Два агента  
    COMPLEX = 3     # Полная цепочка

class DelegationEngine:
    def __init__(self):
        self.agent_capabilities = {
            'dashka': ['coordination', 'ui_design', 'project_management'],
            'claude': ['analysis', 'architecture', 'planning'],
            'deepseek': ['coding', 'implementation', 'debugging']
        }
        
    async def route_task(self, task_text: str) -> List[str]:
        """Определяет оптимальную цепочку агентов для задачи"""
        complexity = self._analyze_complexity(task_text)
        
        if complexity == TaskComplexity.SIMPLE:
            return [self._select_best_agent(task_text)]
        elif complexity == TaskComplexity.MEDIUM:
            return ['claude', 'deepseek']  # Анализ + Реализация
        else:
            return ['dashka', 'claude', 'deepseek', 'dashka']  # Полный цикл
    
    def _analyze_complexity(self, task: str) -> TaskComplexity:
        # Простая логика определения сложности
        if any(word in task.lower() for word in ['implement', 'code', 'build']):
            return TaskComplexity.COMPLEX
        elif any(word in task.lower() for word in ['analyze', 'plan']):
            return TaskComplexity.MEDIUM
        return TaskComplexity.SIMPLE