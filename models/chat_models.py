# models/chat_models.py
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel
import uuid

class Message(BaseModel):
    id: str = None
    sender: Literal["user", "agent"] = "user"
    text: str
    timestamp: datetime = None
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    project_id: Optional[str] = None
    
    def __init__(self, **data):
        if data.get('id') is None:
            data['id'] = str(uuid.uuid4())
        if data.get('timestamp') is None:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

class Project(BaseModel):
    id: str = None
    name: str
    description: Optional[str] = ""
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True
    chat_count: int = 0
    
    def __init__(self, **data):
        if data.get('id') is None:
            data['id'] = str(uuid.uuid4())
        if data.get('created_at') is None:
            data['created_at'] = datetime.now()
        if data.get('updated_at') is None:
            data['updated_at'] = datetime.now()
        super().__init__(**data)

class ChatSession(BaseModel):
    id: str = None
    project_id: str
    agent_id: str
    agent_name: str
    created_at: datetime = None
    messages: List[Message] = []
    is_active: bool = True
    
    def __init__(self, **data):
        if data.get('id') is None:
            data['id'] = str(uuid.uuid4())
        if data.get('created_at') is None:
            data['created_at'] = datetime.now()
        super().__init__(**data)

class Agent(BaseModel):
    id: str
    name: str
    description: str
    emoji: str
    color: str
    is_online: bool = True
    capabilities: List[str] = []

# Предустановленные агенты
AGENTS = {
    "dashka": Agent(
        id="dashka",
        name="Dashka",
        description="Координатор и UI-специалист",
        emoji="🤖",
        color="bg-purple-500",
        capabilities=["coordination", "ui_design", "project_management"]
    ),
    "claude": Agent(
        id="claude",
        name="Claude",
        description="Аналитик и архитектор",
        emoji="🧠",
        color="bg-blue-500",
        capabilities=["analysis", "architecture", "planning"]
    ),
    "deepseek": Agent(
        id="deepseek",
        name="DeepSeek",
        description="Инженер и разработчик",
        emoji="💻",
        color="bg-green-500",
        capabilities=["coding", "implementation", "debugging"]
    )
}

class ChatRequest(BaseModel):
    message: str
    agent_id: str
    project_id: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    message_id: str
    response: str
    agent_id: str
    agent_name: str
    timestamp: datetime
    success: bool = True
    error: Optional[str] = None