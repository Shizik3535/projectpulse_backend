from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ProjectStatus(Base):
    __tablename__ = "project_statuses"

    # Атрибуты
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Связи
    projects = relationship("Project", back_populates="status")


class Project(Base):
    __tablename__ = "projects"

    # Атрибуты
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    
    # Внешние ключи
    status_id = Column(Integer, ForeignKey('project_statuses.id'), nullable=False, default=1)
    
    # Связи
    tasks = relationship("Task", back_populates="project")
    status = relationship("ProjectStatus", back_populates="projects", lazy="joined")
    members = relationship("ProjectMember", back_populates="project")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)


class ProjectMember(Base):
    __tablename__ = "project_members"

    # Атрибуты
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete="CASCADE"), nullable=False)

    # Связи
    user = relationship("User", back_populates="assigned_projects")
    project = relationship("Project", back_populates="members")
