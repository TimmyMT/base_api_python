from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_digest = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String, nullable=False, default="user")

    refresh_tokens = relationship("RefreshToken", back_populates="user")
