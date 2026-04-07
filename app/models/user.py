from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from app.models.association_tables import user_roles

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False, server_default='')
    last_name = Column(String(255), nullable=False, server_default='')
    email = Column(String(255), unique=True, index=True)
    password_digest = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    roles = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users"
    )

    def has_role(self, role_name: str) -> bool:
        return any(role.name == role_name for role in self.roles)

    
