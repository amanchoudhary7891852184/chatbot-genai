from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str

class ChatHistoryBase(BaseModel):
    role: str
    content: str

class ChatHistoryResponse(ChatHistoryBase):
    id: int
    user_id: int
    timestamp: datetime

    model_config = {'from_attributes': True}

class ChatResponse(BaseModel):
    response: str
