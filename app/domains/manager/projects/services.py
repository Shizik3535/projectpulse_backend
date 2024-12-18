from fastapi import HTTPException, status

from app.domains.manager.services import ManagerService
# DAOs
from app.domains.projects.dao import ProjectDAO, ProjectMemberDAO, ProjectStatusDAO
from app.domains.users.dao import UserDAO
# Схемы
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.tasks.schemas import TaskResponse
from app.domains.projects.schemas import (
    # Ответы
    ProjectResponse,
    # Запросы
    ProjectCreate,
    ProjectUpdate
)
from app.base.schemas import MessageResponse


class ManagerProjectService(ManagerService):
    @classmethod
    async def get_projects(
        cls,
        current_user: UserDB
    ):
        cls._check_role(current_user.role.name)
        projects = await ProjectDAO.find_all()
        return [
            ProjectResponse(
                id=project.id,
                title=project.title,
                description=project.description,
                start_date=project.start_date,
                due_date=project.due_date,
                status=project.status.name
            ) for project in projects
        ]

    @classmethod
    async def get_project(
        cls,
        project_id: int,
        current_user: UserDB
    ) -> ProjectResponse:
        cls._check_role(current_user.role.name)
        project = await ProjectDAO.find_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
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
    async def create_project(
        cls,
        project_data: ProjectCreate,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        await ProjectDAO.create(
            title=project_data.title,
            description=project_data.description,
            start_date=project_data.start_date,
            due_date=project_data.due_date,
        )
        return MessageResponse(
            message="Проект успешно создан"
        )
        
    @classmethod
    async def update_project(
        cls,
        project_id: int, 
        project_data: ProjectUpdate,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if not await ProjectDAO.find_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        if not await ProjectStatusDAO.find_by_id(project_data.status_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Статус не найден"
            )
        await ProjectDAO.update(
            model_id=project_id,
            title=project_data.title,
            description=project_data.description,
            start_date=project_data.start_date,
            due_date=project_data.due_date,
            status_id=project_data.status_id
        )
        return MessageResponse(
            message="Проект успешно обновлен"
        )

    @classmethod
    async def delete_project(
        cls,
        project_id: int,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if not await ProjectDAO.find_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        await ProjectDAO.delete(model_id=project_id)
        return MessageResponse(
            message="Проект успешно удален"
        )

    @classmethod
    async def get_project_members(
        cls,
        project_id: int,
        current_user: UserDB
    ) -> list[UserResponse]:
        cls._check_role(current_user.role.name)
        project_members = await ProjectMemberDAO.get_project_members(project_id)
        return [
            UserResponse(
                id=user.user.id,
                first_name=user.user.first_name,
                last_name=user.user.last_name,
                patronymic=user.user.patronymic,
                role=user.user.role.name,
                position=user.user.position.name if user.user.position else None
            ) for user in project_members
        ]

    @classmethod
    async def add_project_member(
        cls,
        project_id: int,
        user_id: int,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        if not await ProjectDAO.find_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        if await ProjectMemberDAO.find_one_or_none(
            project_id=project_id,
            user_id=user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже добавлен в проект"
            )
        await ProjectMemberDAO.create(
            project_id=project_id,
            user_id=user_id
        )
        return MessageResponse(
            message="Пользователь успешно добавлен в проект"
        )

    @classmethod
    async def remove_project_member(
        cls,
        project_id: int,
        user_id: int,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        if not await ProjectDAO.find_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        if not await ProjectMemberDAO.find_one_or_none(
            project_id=project_id,
            user_id=user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден в проекте"
            )
        await ProjectMemberDAO.delete_by_filter(
            project_id=project_id,
            user_id=user_id
        )
        return MessageResponse(
            message="Пользователь успешно удален из проекта"
        )

    @classmethod
    async def get_project_tasks(
        cls,
        project_id: int,
        current_user: UserDB
    ):
        cls._check_role(current_user.role.name)
        if not await ProjectDAO.find_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
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