from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import datetime as dt

def utcnow():
    return dt.datetime.now(dt.timezone.utc)

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(50)) # user or assistant
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=utcnow)

    user = relationship("Users", back_populates="chats")
