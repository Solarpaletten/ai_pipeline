"""
🚀 Level 7: DelegationEngine v1.0
Умная маршрутизация задач между AI агентами
"""
from typing import Dict, List, Optional
from enum import Enum
import re

class TaskComplexity(Enum):
    SIMPLE = 1      # Один агент
    MEDIUM = 2      # Два агента  
    COMPLEX = 3     # Полная цепочка

class DelegationEngine:
    def __init__(self):
        self.agent_capabilities = {
            'dashka': {
                'skills': ['coordination', 'ui_design', 'project_management', 'presentation'],
                'keywords': ['координация', 'ui', 'дизайн', 'интерфейс', 'управление']
            },
            'claude': {
                'skills': ['analysis', 'architecture', 'planning', 'documentation'],
                'keywords': ['анализ', 'архитектура', 'план', 'структура', 'документация']
            },
            'deepseek': {
                'skills': ['coding', 'implementation', 'debugging', 'optimization'],
                'keywords': ['код', 'программирование', 'реализация', 'разработка', 'баг']
            }
        }
        
    async def route_task(self, task_text: str) -> Dict:
        """🎯 Определяет оптимальную цепочку агентов для задачи"""
        complexity = self._analyze_complexity(task_text)
        chain = self._generate_chain(task_text, complexity)
        
        return {
            'task': task_text,
            'complexity': complexity.name,
            'recommended_chain': chain,
            'reasoning': self._explain_routing(task_text, chain),
            'estimated_time': len(chain) * 5,  # 5 мин на агента
            'level': 7
        }
    
    def _analyze_complexity(self, task: str) -> TaskComplexity:
        """📊 Анализ сложности задачи"""
        task_lower = task.lower()
        
        # Подсчитываем ключевые слова
        complexity_indicators = 0
        
        if any(word in task_lower for word in ['создать', 'построить', 'разработать', 'implement']):
            complexity_indicators += 2
            
        if any(word in task_lower for word in ['анализ', 'план', 'архитектура', 'analyze']):
            complexity_indicators += 1
            
        if any(word in task_lower for word in ['интеграция', 'система', 'полный', 'complete']):
            complexity_indicators += 2
            
        if complexity_indicators >= 3:
            return TaskComplexity.COMPLEX
        elif complexity_indicators >= 1:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _generate_chain(self, task: str, complexity: TaskComplexity) -> List[str]:
        """🔗 Генерация цепочки агентов"""
        task_lower = task.lower()
        
        if complexity == TaskComplexity.SIMPLE:
            # Выбираем лучшего агента для простой задачи
            if any(word in task_lower for word in self.agent_capabilities['dashka']['keywords']):
                return ['dashka']
            elif any(word in task_lower for word in self.agent_capabilities['claude']['keywords']):
                return ['claude']
            else:
                return ['deepseek']
                
        elif complexity == TaskComplexity.MEDIUM:
            # Комбинация двух агентов
            if any(word in task_lower for word in ['код', 'разработка', 'implementation']):
                return ['claude', 'deepseek']  # Анализ + Реализация
            else:
                return ['dashka', 'claude']   # Координация + Планирование
                
        else:  # COMPLEX
            # Полная цепочка делегирования
            return ['dashka', 'claude', 'deepseek', 'dashka']
    
    def _explain_routing(self, task: str, chain: List[str]) -> str:
        """💡 Объяснение логики маршрутизации"""
        explanations = {
            'dashka': 'координация и управление проектом',
            'claude': 'анализ и архитектурное планирование', 
            'deepseek': 'техническая реализация и разработка'
        }
        
        if len(chain) == 1:
            return f"Простая задача → {explanations[chain[0]]}"
        elif len(chain) == 2:
            return f"Средняя сложность → {explanations[chain[0]]} + {explanations[chain[1]]}"
        else:
            return "Комплексная задача → полный цикл делегирования"

# Создаем глобальный экземпляр
delegation_engine = DelegationEngine()
