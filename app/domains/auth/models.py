from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class BlackListToken(Base):
    __tablename__ = "blacklist_tokens"

    # Атрибуты
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
