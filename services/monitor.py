"""
Сервис мониторинга агентов
"""
import asyncio
import aiohttp
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AgentMonitor:
    def __init__(self):
        self.agents_status = {}
        self.check_interval = 30  # секунд
        
    async def start_monitoring(self):
        """Запуск непрерывного мониторинга"""
        while True:
            await self.check_all_agents()
            await asyncio.sleep(self.check_interval)
    
    async def check_all_agents(self):
        """Проверка всех агентов"""
        try:
            # Проверяем Telegram
            telegram_status = await self._check_telegram()
            self.agents_status['dashka'] = telegram_status
            
            # Проверяем Claude (упрощенно)
            claude_status = self._check_claude()
            self.agents_status['claude'] = claude_status
            
            # Проверяем DeepSeek (упрощенно)
            deepseek_status = self._check_deepseek()
            self.agents_status['deepseek'] = deepseek_status
            
            logger.info(f"Мониторинг завершен: {len(self.agents_status)} агентов")
            
        except Exception as e:
            logger.error(f"Ошибка мониторинга: {e}")
    
    async def _check_telegram(self) -> Dict[str, Any]:
        """Проверка Telegram API"""
        import os
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not token:
            return {"online": False, "error": "No token"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.telegram.org/bot{token}/getMe') as resp:
                    return {
                        "online": resp.status == 200,
                        "status_code": resp.status,
                        "last_check": datetime.utcnow().isoformat()
                    }
        except Exception as e:
            return {"online": False, "error": str(e)}
    
    def _check_claude(self) -> Dict[str, Any]:
        """Проверка Claude (упрощенная)"""
        import os
        api_key = os.getenv('ANTHROPIC_API_KEY')
        return {
            "online": bool(api_key),
            "token_valid": len(api_key or '') > 20,
            "last_check": datetime.utcnow().isoformat()
        }
    
    def _check_deepseek(self) -> Dict[str, Any]:
        """Проверка DeepSeek (упрощенная)"""
        import os
        api_key = os.getenv('DEEPSEEK_API_KEY')
        return {
            "online": bool(api_key),
            "token_valid": len(api_key or '') > 20,
            "last_check": datetime.utcnow().isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Получить текущий статус всех агентов"""
        return self.agents_status
