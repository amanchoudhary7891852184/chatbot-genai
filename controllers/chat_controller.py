from sqlalchemy.ext.asyncio import AsyncSession
from models.chat import ChatHistory
from services.chat_service import get_chat_response
from schemas import chat_schemas

from sqlalchemy import select, desc

async def chat(message: str, user_id: int, db: AsyncSession):
    # Fetch recent history (e.g., last 5 messages)
    result = await db.execute(
        select(ChatHistory)
        .where(ChatHistory.user_id == user_id)
        .order_by(desc(ChatHistory.timestamp))
        .limit(5)
    )
    history = result.scalars().all()
    history = list(reversed(history)) # Order chronologically

    # Get response
    response_text = get_chat_response(message, history)
    
    # Save to DB
    user_msg = ChatHistory(user_id=user_id, role="user", content=message)
    bot_msg = ChatHistory(user_id=user_id, role="assistant", content=response_text)
    
    db.add(user_msg)
    db.add(bot_msg)
    await db.commit()
    
    return chat_schemas.ChatResponse(response=response_text)
