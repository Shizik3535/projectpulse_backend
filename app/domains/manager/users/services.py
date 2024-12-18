from fastapi import HTTPException, status

from app.core.security import Security
from app.domains.manager.services import ManagerService

# DAOs
from app.domains.users.dao import UserDAO, PositionDAO, RoleDAO
from app.domains.projects.dao import ProjectMemberDAO
from app.domains.tasks.dao import TaskAssignmentDAO

# Схемы
from app.domains.users.schemas import (
    # Базовые
    UserDB,
    # Ответы
    UserResponse,
    # Запросы
    UserCreate,
    UserUpdate,
)
from app.domains.projects.schemas import ProjectResponse
from app.domains.tasks.schemas import TaskResponseWithProject
from app.base.schemas import MessageResponse


class ManagerUserService(ManagerService):
    @classmethod
    async def get_users(
            cls,
            current_user: UserDB
    ) -> list[UserResponse]:
        cls._check_role(current_user.role.name)
        users = await UserDAO.find_all()
        return [
            UserResponse(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                patronymic=user.patronymic,
                role=user.role.name,
                position=user.position.name if user.position else None
            ) for user in users
        ]

    @classmethod
    async def get_user(
            cls,
            user_id: int,
            current_user: UserDB
    ) -> UserResponse:
        cls._check_role(current_user.role.name)
        user = await UserDAO.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
            role=user.role.name,
            position=user.position.name if user.position else None
        )

    @classmethod
    async def create_user(
            cls,
            user_data: UserCreate,
            current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if await UserDAO.find_one_or_none(username=user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким логином уже существует"
            )
        if user_data.position_id and not await PositionDAO.find_by_id(user_data.position_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Должность не найдена"
            )
        await UserDAO.create(
            username=user_data.username,
            hashed_password=Security.get_hashed_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            patronymic=user_data.patronymic,
            position_id=user_data.position_id
        )
        return MessageResponse(
            message="Пользователь успешно создан"
        )

    @classmethod
    async def delete_user(
            cls,
            user_id: int,
            current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if current_user.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нельзя удалить самого себя"
            )
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        await UserDAO.delete(user_id)
        return MessageResponse(
            message="Пользователь успешно удален"
        )

    @classmethod
    async def update_user(
            cls,
            user_id: int,
            user_data: UserUpdate,
            current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        if user_data.position_id and not await PositionDAO.find_by_id(user_data.position_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Должность не найдена"
            )
        if not await RoleDAO.find_by_id(user_data.role_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Роль не найдена"
            )
        if current_user.id == user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нельзя обновить самого себя"
            )
        await UserDAO.update(
            user_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            patronymic=user_data.patronymic,
            role_id=user_data.role_id,
            position_id=user_data.position_id
        )
        return MessageResponse(
            message="Пользователь успешно обновлен"
        )

    @classmethod
    async def get_user_tasks(
            cls,
            user_id: int,
            current_user: UserDB
    ):
        cls._check_role(current_user.role.name)
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        tasks = await TaskAssignmentDAO.get_user_tasks(user_id)
        return [
            TaskResponseWithProject(
                id=task.task.id,
                title=task.task.title,
                description=task.task.description,
                status=task.task.status.name,
                due_date=task.task.due_date,
                priority=task.task.priority.name,
                start_date=task.task.start_date,
                project=ProjectResponse(
                        id=task.task.project.id,
                        title=task.task.project.title,
                        description=task.task.project.description,
                        start_date=task.task.project.start_date,
                        due_date=task.task.project.due_date,
                        status=task.task.project.status.name,
                    ) if task.task.project else None,
            ) for task in tasks
        ]

    @classmethod
    async def get_user_projects(
            cls,
            user_id: int,
            current_user: UserDB
    ):
        cls._check_role(current_user.role.name)
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        projects = await ProjectMemberDAO.get_user_projects(user_id)
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
