from fastapi import APIRouter, Depends

from app.core.security import Security

# Сервисы
from app.domains.users.services import UserService
from app.domains.tasks.services import TaskService
from app.domains.projects.services import ProjectService

# Схемы
from app.base.schemas import ErrorResponse
from app.domains.users.schemas import UserDB, PositionResponse, RoleResponse
from app.domains.tasks.schemas import StatusResponse as StatusTaskResponse, PriorityResponse
from app.domains.projects.schemas import StatusResponse as StatusProjectResponse


router = APIRouter(
    prefix="/references",
    tags=["Справочные данные"]
)


@router.get(
    path="/positions",
    summary="Получение списка должностей",
    responses={
        200: {
            "description": "Список должностей получен успешно",
            "model": list[PositionResponse]
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_positions(
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех должностей в компании"""
    return await UserService.get_all_positions()


@router.get(
    path="/roles",
    summary="Получение списка ролей",
    responses={
        200: {
            "description": "Список ролей получен успешно",
            "model": list[RoleResponse]
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_roles(
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех ролей в компании"""
    return await UserService.get_all_roles()


@router.get(
    path="/task-statuses",
    summary="Получение списка статусов задач",
    responses={
        200: {
            "description": "Список статусов задач получен успешно",
            "model": list[StatusTaskResponse]
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_task_statuses(
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех статусов задач"""
    return await TaskService.get_all_statuses()


@router.get(
    path="/task-priorities",
    summary="Получение списка приоритетов задач",
    responses={
        200: {
            "description": "Список приоритетов задач получен успешно",
            "model": list[PriorityResponse]
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_task_priorities(
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех приоритетов задач"""
    return await TaskService.get_all_priorities()


@router.get(
    path="/project-statuses",
    summary="Получение списка статусов проектов",
    responses={
        200: {
            "description": "Список статусов проектов получен успешно",
            "model": list[StatusProjectResponse]
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_project_statuses(
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех статусов проектов"""
    return await ProjectService.get_all_statuses()
