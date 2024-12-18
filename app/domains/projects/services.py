from fastapi import HTTPException, status

# DAOs
from app.domains.projects.dao import ProjectStatusDAO, ProjectDAO, ProjectMemberDAO

# Схемы
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.projects.schemas import ProjectResponse
from app.domains.tasks.schemas import TaskResponse


class ProjectService:
    @classmethod
    async def get_all_statuses(cls):
        return await ProjectStatusDAO.find_all()
    
    @classmethod
    async def get_user_projects(cls, current_user: UserDB):
        projects = await ProjectMemberDAO.get_user_projects(user_id=current_user.id)
        return [
            ProjectResponse(
                id=project.project.id,
                title=project.project.title,
                description=project.project.description,
                start_date=project.project.start_date,
                due_date=project.project.due_date,
                status=project.project.status.name
            ) for project in projects
        ]
    
    @classmethod
    async def get_project(cls, project_id: int, current_user: UserDB):
        project = await ProjectDAO.find_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        if not await ProjectMemberDAO.find_one_or_none(
            project_id=project_id,
            user_id=current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не являетесь участником проекта"
            )
        return ProjectResponse(
            id=project.id,
            title=project.title,
            description=project.description,
            start_date=project.start_date,
            due_date=project.due_date,
            status=project.status.name
        )
        
    @classmethod
    async def get_project_tasks(cls, project_id: int, current_user: UserDB):
        if not await ProjectDAO.find_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        if not await ProjectMemberDAO.find_one_or_none(
            project_id=project_id,
            user_id=current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не являетесь участником проекта"
            )
        tasks = await ProjectDAO.get_project_tasks(project_id=project_id)
        tasks = tasks.tasks
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                start_date=task.start_date,
                due_date=task.due_date,
                status=task.status.name,
                priority=task.priority.name
            )
            for task in tasks
        ]
        
    @classmethod
    async def get_project_members(cls, project_id: int, current_user: UserDB):
        if not await ProjectDAO.find_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        if not await ProjectMemberDAO.find_one_or_none(
            project_id=project_id,
            user_id=current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не являетесь участником проекта"
            )
        members = await ProjectMemberDAO.get_project_members(project_id=project_id)
        return [
            UserResponse(
                id=member.user.id,
                first_name=member.user.first_name,
                last_name=member.user.last_name,
                patronymic=member.user.patronymic,
                role=member.user.role.name,
                position=member.user.position.name if member.user.position else None
            )
            for member in members
        ]