from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TaskPriority(Base):
    __tablename__ = "task_priorities"

    # Атрибуты
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Связи
    tasks = relationship("Task", back_populates="priority")


class TaskStatus(Base):
    __tablename__ = "task_statuses"

    # Атрибуты
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Связи
    tasks = relationship("Task", back_populates="status")


class Task(Base):
    __tablename__ = "tasks"

    # Атрибуты
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    
    # Внешние ключи
    project_id = Column(Integer, ForeignKey('projects.id', ondelete="CASCADE"), nullable=True, default=None)
    status_id = Column(Integer, ForeignKey('task_status.id'), nullable=False, default=1)
    priority_id = Column(Integer, ForeignKey('task_priority.id'), nullable=False, default=1)
    
    # Связи
    project = relationship("Project", back_populates="tasks")
    status = relationship("TaskStatus", back_populates="tasks", lazy="joined")
    priority = relationship("TaskPriority", back_populates="tasks", lazy="joined")
    assigned_users = relationship("TaskAssignment", back_populates="task")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)


class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    # Атрибуты
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete="CASCADE"), nullable=False)

    # Внешние ключи
    user = relationship("User", back_populates="assigned_tasks")
    task = relationship("Task", back_populates="assigned_users")
