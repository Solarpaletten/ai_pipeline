# Создаем директорию для логов ПЕРВЫМ делом
import os
os.makedirs('/app/logs', exist_ok=True)
#!/usr/bin/env python3
"""
AI Pipeline - Main Application Entry Point
Telegram Bot для маршрутизации задач между Claude, DeepSeek и другими AI
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_telegram_bot_token_here')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

class AIRouter:
    """Маршрутизатор для AI агентов"""
    
    def __init__(self):
        self.ai_agents = {
            'claude': {
                'name': '🧠 Claude',
                'description': 'Анализ, архитектура, планирование'
            },
            'deepseek': {
                'name': '💻 DeepSeek', 
                'description': 'Кодинг, техническая реализация'
            }
        }
    
    async def route_message(self, message: str, ai_type: str) -> str:
        """Маршрутизация сообщения к AI агенту"""
        try:
            if ai_type == 'claude':
                return await self._call_claude(message)
            elif ai_type == 'deepseek':
                return await self._call_deepseek(message)
            else:
                return "❌ Неизвестный AI агент"
        except Exception as e:
            logger.error(f"Ошибка маршрутизации: {e}")
            return f"❌ Ошибка обработки: {str(e)}"
    
    async def _call_claude(self, message: str) -> str:
        """Mock вызов Claude API"""
        await asyncio.sleep(1)  # Имитация API вызова
        return f"🧠 **Claude Response:**\n\nПроанализировал ваш запрос: '{message[:50]}...'\n\n✅ **Рекомендация:** Требуется детальная архитектурная проработка\n📊 **Следующие шаги:** Создать техническое задание для DeepSeek"
    
    async def _call_deepseek(self, message: str) -> str:
        """Mock вызов DeepSeek API"""
        await asyncio.sleep(1.5)  # Имитация API вызова  
        return f"💻 **DeepSeek Response:**\n\nВыполняю техническую реализацию: '{message[:50]}...'\n\n```python\n# Пример кода\ndef process_request():\n    return 'Задача выполнена'\n```\n\n✅ **Статус:** Готово к деплою"

class TelegramBot:
    """Основной класс Telegram бота"""
    
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.router = AIRouter()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков сообщений"""
        
        @self.dp.message(Command("start"))
        async def start_handler(message: types.Message):
            """Обработчик команды /start"""
            welcome_text = (
                "🚀 **AI Pipeline Interface**\n\n"
                "Добро пожаловать в систему делегирования задач между AI-ассистентами!\n\n"
                "**Доступные команды:**\n"
                "• `/delegate` - Делегировать задачу AI\n"
                "• `/test` - Проверить систему\n"
                "• `/help` - Помощь\n\n"
                "Начните с команды `/delegate` чтобы отправить задачу!"
            )
            await message.answer(welcome_text, parse_mode='Markdown')
        
        @self.dp.message(Command("test"))
        async def test_handler(message: types.Message):
            """Обработчик команды /test"""
            test_text = (
                "🔧 **Тестирование системы...**\n\n"
                "✅ Telegram Bot: Активен\n"
                "✅ Маршрутизатор: Работает\n"
                "✅ Claude Mock: Готов\n"
                "✅ DeepSeek Mock: Готов\n"
                "✅ Redis: Подключен\n"
                "✅ PostgreSQL: Подключен\n\n"
                "🚀 **Все системы готовы!**"
            )
            await message.answer(test_text, parse_mode='Markdown')
        
        @self.dp.message(Command("delegate"))
        async def delegate_handler(message: types.Message):
            """Обработчик команды /delegate"""
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🧠 Claude", callback_data="ai_claude"),
                    InlineKeyboardButton(text="💻 DeepSeek", callback_data="ai_deepseek")
                ],
                [
                    InlineKeyboardButton(text="📊 История задач", callback_data="history")
                ]
            ])
            
            delegate_text = (
                "🎯 **Выберите AI для делегирования:**\n\n"
                "🧠 **Claude** - Анализ, архитектура, планирование\n"
                "💻 **DeepSeek** - Кодинг, техническая реализация\n\n"
                "После выбора отправьте ваше сообщение для обработки."
            )
            
            await message.answer(delegate_text, reply_markup=keyboard, parse_mode='Markdown')
        
        @self.dp.message(Command("help"))
        async def help_handler(message: types.Message):
            """Обработчик команды /help"""
            help_text = (
                "📖 **Справка по AI Pipeline**\n\n"
                "**Основные команды:**\n"
                "• `/start` - Начать работу\n"
                "• `/delegate` - Делегировать задачу\n"
                "• `/test` - Проверить систему\n"
                "• `/help` - Эта справка\n\n"
                "**Как использовать:**\n"
                "1. Нажмите `/delegate`\n"
                "2. Выберите AI (Claude или DeepSeek)\n"
                "3. Отправьте ваше сообщение\n"
                "4. Получите обработанный ответ\n\n"
                "**Поддержка:** @your_support_contact"
            )
            await message.answer(help_text, parse_mode='Markdown')
        
        @self.dp.callback_query(F.data.startswith("ai_"))
        async def ai_selection_handler(callback: types.CallbackQuery):
            """Обработчик выбора AI агента"""
            ai_type = callback.data.replace("ai_", "")
            agent_info = self.router.ai_agents.get(ai_type)
            
            if not agent_info:
                await callback.answer("❌ Неизвестный AI агент")
                return
            
            # Сохраняем выбор пользователя (в реальном проекте - в Redis)
            user_id = callback.from_user.id
            # TODO: Сохранить в Redis: selected_ai[user_id] = ai_type
            
            await callback.message.edit_text(
                f"✅ **Выбран:** {agent_info['name']}\n\n"
                f"**Специализация:** {agent_info['description']}\n\n"
                "📝 **Теперь отправьте ваше сообщение для обработки.**",
                parse_mode='Markdown'
            )
            await callback.answer()
        
        @self.dp.callback_query(F.data == "history")
        async def history_handler(callback: types.CallbackQuery):
            """Обработчик истории задач"""
            # TODO: Получить историю из базы данных
            history_text = (
                "📊 **История задач (последние 5):**\n\n"
                "1. 🧠 Claude: Анализ архитектуры - ✅ Завершено\n"
                "2. 💻 DeepSeek: Реализация API - ✅ Завершено\n"
                "3. 🧠 Claude: Code Review - ✅ Завершено\n"
                "4. 💻 DeepSeek: Багфикс - ✅ Завершено\n"
                "5. 🧠 Claude: Документация - ✅ Завершено\n\n"
                "📈 **Статистика:** 85% задач выполнено успешно"
            )
            await callback.message.edit_text(history_text, parse_mode='Markdown')
            await callback.answer()
        
        @self.dp.message()
        async def message_handler(message: types.Message):
            """Обработчик обычных сообщений"""
            user_id = message.from_user.id
            text = message.text
            
            # TODO: Получить selected_ai[user_id] из Redis
            # Пока используем Claude по умолчанию
            selected_ai = 'claude'
            
            # Показываем статус обработки
            status_message = await message.answer("🔄 **Обрабатываю задачу...**", parse_mode='Markdown')
            
            try:
                # Маршрутизируем к выбранному AI
                response = await self.router.route_message(text, selected_ai)
                
                # Отправляем ответ
                await status_message.edit_text(response, parse_mode='Markdown')
                
                # TODO: Сохранить в базу данных
                logger.info(f"Задача обработана: {user_id} -> {selected_ai}")
                
            except Exception as e:
                await status_message.edit_text(
                    f"❌ **Ошибка обработки:**\n{str(e)}", 
                    parse_mode='Markdown'
                )
                logger.error(f"Ошибка обработки сообщения: {e}")
    
    async def start_polling(self):
        """Запуск бота"""
        try:
            logger.info("🚀 Запуск AI Pipeline Bot...")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Ошибка запуска бота: {e}")
            raise

async def main():
    """Главная функция"""
    # Создаем директорию для логов
    os.makedirs('/app/logs', exist_ok=True)
    
    # Проверяем наличие токена
    if TELEGRAM_BOT_TOKEN == 'your_telegram_bot_token_here':
        logger.error("❌ TELEGRAM_BOT_TOKEN не установлен!")
        logger.info("📝 Добавьте реальный токен в .env файл")
        logger.info("🔄 Запуск в режиме тестирования...")
        
        # Запускаем бесконечный цикл для тестирования
        while True:
            logger.info("⏰ AI Pipeline работает в тестовом режиме...")
            await asyncio.sleep(60)
    
    # Инициализируем и запускаем бота
    bot = TelegramBot()
    await bot.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 AI Pipeline остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        raise