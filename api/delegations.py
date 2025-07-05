"""
API для работы с делегированиями
"""
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/delegations", tags=["delegations"])

class Delegation(BaseModel):
    from_agent: str
    to_agent: str
    message: str
    user_id: int

# Временное хранилище
delegations_storage = []

@router.get("/recent")
async def get_recent():
    """Последние делегирования"""
    return delegations_storage[-50:]

@router.post("/log")
async def log_delegation(delegation: Delegation):
    """Логирование нового делегирования"""
    entry = {
        "id": len(delegations_storage) + 1,
        "timestamp": datetime.utcnow().isoformat(),
        **delegation.dict()
    }
    delegations_storage.append(entry)
    return {"status": "logged", "id": entry["id"]}
