# services/ai_integrations.py
"""
Реальные интеграции с AI API
"""

import asyncio
import logging
import os
import httpx
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ClaudeService:
    """Реальная интеграция с Claude API"""
    
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY')
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    async def send_message(self, message: str, context: str = "") -> str:
        """Отправка сообщения Claude"""
        if not self.api_key:
            return "❌ Claude API ключ не настроен"
        
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{context}\n\n{message}" if context else message
                        }
                    ]
                }
                
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['content'][0]['text']
                else:
                    logger.error(f"Claude API error: {response.status_code} - {response.text}")
                    return f"❌ Claude API ошибка: {response.status_code}"
                    
        except Exception as e:
            logger.error(f"Claude API exception: {e}")
            return f"❌ Ошибка Claude: {str(e)}"

class DeepSeekService:
    """Реальная интеграция с DeepSeek API"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def send_message(self, message: str, context: str = "") -> str:
        """Отправка сообщения DeepSeek"""
        if not self.api_key:
            return "❌ DeepSeek API ключ не настроен"
        
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "model": "deepseek-coder",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Ты - опытный разработчик и архитектор ПО. Отвечай на русском языке, предоставляй практические решения и код."
                        },
                        {
                            "role": "user", 
                            "content": f"{context}\n\n{message}" if context else message
                        }
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.1
                }
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content']
                else:
                    logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                    return f"❌ DeepSeek API ошибка: {response.status_code}"
                    
        except Exception as e:
            logger.error(f"DeepSeek API exception: {e}")
            return f"❌ Ошибка DeepSeek: {str(e)}"

class DashkaService:
    """Dashka - координатор команды (логика на основе правил)"""
    
    async def send_message(self, message: str, context: str = "") -> str:
        """Обработка сообщения Dashka"""
        
        # Анализ типа задачи
        if any(word in message.lower() for word in ['код', 'программ', 'функци', 'класс', 'api']):
            return (
                "🤖 **Dashka:** Вижу техническую задачу!\n\n"
                "📋 **Мой план:**\n"
                "1. Сначала отправлю задачу Claude для архитектурного анализа\n"
                "2. Затем DeepSeek реализует техническое решение\n"
                "3. Проконтролирую качество и соответствие требованиям\n\n"
                "⚡ **Действие:** Направляю задачу команде разработки!"
            )
        
        elif any(word in message.lower() for word in ['анализ', 'план', 'стратег', 'архитектур']):
            return (
                "🤖 **Dashka:** Это аналитическая задача!\n\n"
                "🧠 **Решение:** Направляю Claude для глубокого анализа\n"
                "📊 **Результат:** Получите структурированные рекомендации\n\n"
                "✅ **Статус:** Задача передана аналитику!"
            )
        
        else:
            return (
                "🤖 **Dashka:** Принял вашу задачу!\n\n"
                "🎯 **Анализирую:**\n"
                f"- Запрос: {message[:100]}...\n"
                "- Приоритет: Средний\n"
                "- Ответственный: Назначается\n\n"
                "⏳ **Статус:** В обработке командой AI Pipeline"
            )

class AIServiceRouter:
    """Роутер для выбора правильного AI сервиса"""
    
    def __init__(self):
        self.claude = ClaudeService()
        self.deepseek = DeepSeekService()
        self.dashka = DashkaService()
        
        self.services = {
            'claude': self.claude,
            'deepseek': self.deepseek,
            'dashka': self.dashka
        }
    
    async def route_message(self, message: str, agent_id: str, context: str = "") -> str:
        """Маршрутизация сообщения к соответствующему AI"""
        
        service = self.services.get(agent_id)
        if not service:
            return f"❌ Неизвестный агент: {agent_id}"
        
        try:
            # Добавляем информацию об агенте в контекст
            agent_context = f"[Агент: {agent_id.upper()}] {context}"
            
            response = await service.send_message(message, agent_context)
            
            # Логируем использование
            logger.info(f"AI Route: {agent_id} | Message length: {len(message)} | Response length: {len(response)}")
            
            return response
            
        except Exception as e:
            logger.error(f"AI routing error for {agent_id}: {e}")
            return f"❌ Ошибка обработки сообщения агентом {agent_id}: {str(e)}"
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Получение статуса всех агентов"""
        status = {}
        
        for agent_id in self.services.keys():
            if agent_id == 'claude':
                status[agent_id] = {
                    "online": bool(self.claude.api_key),
                    "type": "external_api"
                }
            elif agent_id == 'deepseek':
                status[agent_id] = {
                    "online": bool(self.deepseek.api_key),
                    "type": "external_api"
                }
            elif agent_id == 'dashka':
                status[agent_id] = {
                    "online": True,
                    "type": "internal_logic"
                }
        
        return status

# Глобальный экземпляр роутера
ai_router = AIServiceRouter()