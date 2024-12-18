from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    # Атрибуты
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Связи
    users = relationship("User", back_populates="role")


class Position(Base):
    __tablename__ = "positions"

    # Атрибуты
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Связи
    users = relationship("User", back_populates="position")


class User(Base):
    __tablename__ = "users"

    # Атрибуты
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    
    # Внешние ключи
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, default=1)
    position_id = Column(Integer, ForeignKey('positions.id', ondelete="SET NULL"), nullable=True)
    
    # Связи
    role = relationship("Role", back_populates="users", lazy="joined")
    position = relationship("Position", back_populates="users", lazy="joined")
    assigned_tasks = relationship("TaskAssignment", back_populates="user")
    assigned_projects = relationship("ProjectMember", back_populates="user")

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
