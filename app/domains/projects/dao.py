from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.database import async_session_maker


from app.base.dao import BaseDAO
from app.domains.projects.models import Project, ProjectStatus, ProjectMember


class ProjectDAO(BaseDAO):
    model = Project

    @classmethod
    async def get_project_tasks(cls, project_id: int):
        async with async_session_maker() as session:
            project = await session.execute(
                select(Project)
                .where(Project.id == project_id)
                .options(joinedload(Project.tasks))
            )
            return project.unique().scalar_one_or_none()

class ProjectStatusDAO(BaseDAO):
    model = ProjectStatus

class ProjectMemberDAO(BaseDAO):
    model = ProjectMember

    @classmethod
    async def get_project_members(cls, project_id: int):
        async with async_session_maker() as session:
            project_members = await session.execute(
                select(ProjectMember)
                .where(ProjectMember.project_id == project_id)
                .options(joinedload(ProjectMember.user))
            )
            return project_members.unique().scalars().all()

    @classmethod
    async def get_user_projects(cls, user_id: int):
        async with async_session_maker() as session:
            project_members = await session.execute(
                select(ProjectMember)
                .where(ProjectMember.user_id == user_id)
                .options(joinedload(ProjectMember.project))
            )
            return project_members.unique().scalars().all()
