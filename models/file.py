from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import datetime as dt

def utcnow():
    return dt.datetime.now(dt.timezone.utc)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), default=utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="files")
