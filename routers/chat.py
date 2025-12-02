from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import chat_controller
from utils.deps import get_current_user
from schemas import chat_schemas

router = APIRouter()

@router.post("/chat", response_model=chat_schemas.ChatResponse)
async def chat(request: chat_schemas.ChatRequest, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await chat_controller.chat(request.message, current_user.id, db)
