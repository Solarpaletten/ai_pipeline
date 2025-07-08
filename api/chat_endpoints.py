# api/chat_endpoints.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, List, Optional
import json
import asyncio
from datetime import datetime

from models.chat_models import (
    Message, ChatSession, Project, Agent, AGENTS,
    ChatRequest, ChatResponse
)

router = APIRouter(prefix="/api/chat", tags=["chat"])

# WebSocket connections storage
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

# In-memory storage (в продакшене заменить на базу данных)
projects_db: Dict[str, Project] = {}
chat_sessions_db: Dict[str, ChatSession] = {}
messages_db: Dict[str, List[Message]] = {}

# ============== REST API ENDPOINTS ==============

@router.get("/agents")
async def get_agents():
    """Получить список доступных агентов"""
    return {"agents": list(AGENTS.values())}

@router.get("/projects")
async def get_projects():
    """Получить список проектов"""
    return {"projects": list(projects_db.values())}

@router.post("/projects")
async def create_project(name: str, description: str = ""):
    """Создать новый проект"""
    project = Project(name=name, description=description)
    projects_db[project.id] = project
    return {"project": project}

@router.get("/projects/{project_id}/chats")
async def get_project_chats(project_id: str):
    """Получить все чаты проекта"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_chats = [
        chat for chat in chat_sessions_db.values() 
        if chat.project_id == project_id
    ]
    return {"chats": project_chats}

@router.post("/send")
async def send_message(request: ChatRequest):
    """Отправить сообщение агенту через REST API"""
    try:
        # Создаем сообщение пользователя
        user_message = Message(
            sender="user",
            text=request.message,
            agent_id=request.agent_id,
            project_id=request.project_id
        )
        
        # Сохраняем сообщение
        if request.project_id not in messages_db:
            messages_db[request.project_id] = []
        messages_db[request.project_id].append(user_message)
        
        # Получаем ответ от агента (заглушка)
        agent_response = await process_agent_message(
            request.message, 
            request.agent_id, 
            request.project_id
        )
        
        # Создаем ответное сообщение
        response_message = Message(
            sender="agent",
            text=agent_response,
            agent_id=request.agent_id,
            agent_name=AGENTS[request.agent_id].name,
            project_id=request.project_id
        )
        
        # Сохраняем ответ
        messages_db[request.project_id].append(response_message)
        
        return ChatResponse(
            message_id=response_message.id,
            response=agent_response,
            agent_id=request.agent_id,
            agent_name=AGENTS[request.agent_id].name,
            timestamp=response_message.timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}/messages")
async def get_project_messages(project_id: str, limit: int = 50):
    """Получить сообщения проекта"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_messages = messages_db.get(project_id, [])
    return {"messages": project_messages[-limit:]}

@router.delete("/projects/{project_id}/messages")
async def clear_project_messages(project_id: str):
    """Очистить сообщения проекта"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    messages_db[project_id] = []
    return {"success": True, "message": "Messages cleared"}

# ============== WEBSOCKET ENDPOINT ==============

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint для real-time чата"""
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Создаем сообщение пользователя
            user_message = Message(
                sender="user",
                text=message_data["message"],
                agent_id=message_data["agent_id"],
                project_id=message_data["project_id"]
            )
            
            # Сохраняем сообщение
            project_id = message_data["project_id"]
            if project_id not in messages_db:
                messages_db[project_id] = []
            messages_db[project_id].append(user_message)
            
            # Отправляем подтверждение получения
            await websocket.send_text(json.dumps({
                "type": "message_received",
                "message": user_message.dict()
            }))
            
            # Обрабатываем сообщение агентом
            agent_response = await process_agent_message(
                message_data["message"],
                message_data["agent_id"],
                project_id
            )
            
            # Создаем ответное сообщение
            response_message = Message(
                sender="agent",
                text=agent_response,
                agent_id=message_data["agent_id"],
                agent_name=AGENTS[message_data["agent_id"]].name,
                project_id=project_id
            )
            
            # Сохраняем ответ
            messages_db[project_id].append(response_message)
            
            # Отправляем ответ клиенту
            await websocket.send_text(json.dumps({
                "type": "agent_response",
                "message": response_message.dict()
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "error": str(e)
        }))

# ============== HELPER FUNCTIONS ==============

async def process_agent_message(message: str, agent_id: str, project_id: str) -> str:
    """Обработка сообщения конкретным агентом"""
    
    if agent_id not in AGENTS:
        return "Unknown agent"
    
    agent = AGENTS[agent_id]
    
    # Заглушка для разных агентов
    if agent_id == "dashka":
        return f"🤖 Dashka: Понял! Обрабатываю ваш запрос: '{message}'. Передам команде для выполнения."
    
    elif agent_id == "claude":
        return f"🧠 Claude: Анализирую ваш запрос: '{message}'. Рекомендую структурированный подход к решению."
    
    elif agent_id == "deepseek":
        return f"💻 DeepSeek: Готов к реализации: '{message}'. Начинаю написание кода."
    
    else:
        return f"{agent.emoji} {agent.name}: Получил сообщение: '{message}'"

# Создаем тестовый проект при старте
async def init_test_data():
    """Инициализация тестовых данных"""
    test_project = Project(
        name="Test Project",
        description="Тестовый проект для демонстрации chat widget"
    )
    projects_db[test_project.id] = test_project

# Вызываем при запуске приложения
# init_test_data() - раскомментировать в main.py