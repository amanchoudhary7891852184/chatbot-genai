from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255), unique=True)
    phone = Column(String(50))
    password = Column(String(255))
    profile = Column(String(255))
    is_active = Column(Boolean, default=True)
    chat_bot_url = Column(String(255))

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    files = relationship("UploadedFile", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")
