from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.database import async_session_maker

from app.base.dao import BaseDAO
from app.domains.tasks.models import Task, TaskStatus, TaskPriority, TaskAssignment


class TaskDAO(BaseDAO):
    model = Task

    @classmethod
    async def get_tasks_with_project(cls):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.project))
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def get_task_with_project(cls, task_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == task_id).options(joinedload(cls.model.project))
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
           

class TaskStatusDAO(BaseDAO):
    model = TaskStatus

class TaskPriorityDAO(BaseDAO):
    model = TaskPriority

class TaskAssignmentDAO(BaseDAO):
    model = TaskAssignment

    @classmethod
    async def get_task_assignments(cls, task_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.task_id == task_id).options(joinedload(cls.model.user))
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def get_user_tasks(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.user_id == user_id).options(joinedload(cls.model.task).joinedload(Task.project))
            result = await session.execute(query)
            return result.unique().scalars().all()
