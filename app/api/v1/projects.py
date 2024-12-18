from fastapi import APIRouter, Depends

from app.core.security import Security
from app.domains.projects.services import ProjectService
# Схемы
from app.base.schemas import ErrorResponse
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.projects.schemas import ProjectResponse
from app.domains.tasks.schemas import TaskResponse


router = APIRouter(
    prefix="/projects",
    tags=["Проекты"]
)


@router.get(
    path="/",
    summary="Получение списка проектов",
    responses={
        200: {
            "model": list[ProjectResponse],
            "description": "Список проектов получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_user_projects(
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка проектов текущего пользователя"""
    return await ProjectService.get_user_projects(current_user)


@router.get(
    path="/{project_id}",
    summary="Получение конкретного проекта",
    responses={
        200: {
            "model": ProjectResponse,
            "description": "Проект получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не участвует в проекте"
        },
        404: {
            "model": ErrorResponse,
            "description": "Проект не найден"
        }
    }
)
async def get_project(
        project_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение проекта по ID с проверкой доступа пользователя"""
    return await ProjectService.get_project(project_id, current_user)


@router.get(
    path="/{project_id}/tasks",
    summary="Получение списка задач",
    responses={
        200: {
            "model": list[TaskResponse],
            "description": "Список задач получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не участвует в проекте"
        },
        404: {
            "model": ErrorResponse,
            "description": "Проект не найден"
        }
    }
)
async def get_project_tasks(
        project_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка задач для конкретного проекта"""
    return await ProjectService.get_project_tasks(project_id, current_user)


@router.get(
    path="/{project_id}/members",
    summary="Получение списка участников",
    responses={
        200: {
            "model": list[UserResponse],
            "description": "Список участников получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не участвует в проекте"
        },
        404: {
            "model": ErrorResponse,
            "description": "Проект не найден"
        }
    }
)
async def get_project_members(
        project_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка участников проекта"""
    return await ProjectService.get_project_members(project_id, current_user)