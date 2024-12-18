from fastapi import APIRouter, Depends, status
from app.core.security import Security

# Сервисы
from app.domains.manager.users.services import ManagerUserService

# Схемы
from app.base.schemas import MessageResponse, ErrorResponse
from app.domains.users.schemas import (
    UserDB,
    UserResponse,
    UserCreate,
    UserUpdate
)
from app.domains.projects.schemas import ProjectResponse
from app.domains.tasks.schemas import TaskResponseWithProject

router = APIRouter(
    prefix="/manager/users",
    tags=["Управление пользователями"]
)


@router.get(
    path="",
    summary="Получение списка сотрудников",
    responses={
        200: {
            "model": list[UserResponse],
            "description": "Список сотрудников получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не является менеджером"
        }
    }
)
async def get_users(
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех сотрудников"""
    return await ManagerUserService.get_users(current_user)


@router.get(
    path="/{user_id}",
    summary="Получение сотрудника",
    responses={
        200: {
            "model": UserResponse,
            "description": "Сотрудник получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не является менеджером"
        },
        404: {
            "model": ErrorResponse,
            "description": "Сотрудник не найден"
        }
    }
)
async def get_user(
        user_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение сотрудника по ID"""
    return await ManagerUserService.get_user(user_id, current_user)


@router.post(
    path="",
    summary="Создание сотрудника",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": MessageResponse,
            "description": "Сотрудник успешно создан"
        },
        400: {
            "model": ErrorResponse,
            "description": "Пользователь с таким логином уже существует"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не является менеджером"
        },
        404: {
            "model": ErrorResponse,
            "description": "Сотрудник или должность не найдены"
        }
    }
)
async def create_user(
        user_data: UserCreate,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Создание нового сотрудника"""
    return await ManagerUserService.create_user(user_data, current_user)


@router.put(
    path="/{user_id}",
    summary="Обновление сотрудника",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Сотрудник успешно обновлен"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не является менеджером"
        },
        404: {
            "model": ErrorResponse,
            "description": "Сотрудник, роль или должность не найдены"
        }
    }
)
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Обновление информации о сотруднике"""
    return await ManagerUserService.update_user(user_id, user_data, current_user)


@router.delete(
    path="/{user_id}",
    summary="Удаление сотрудника",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Сотрудник успешно удален"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не является менеджером или попытка удалить себя"
        },
        404: {
            "model": ErrorResponse,
            "description": "Сотрудник не найден"
        }
    }
)
async def delete_user(
        user_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Удаление сотрудника"""
    return await ManagerUserService.delete_user(user_id, current_user)


@router.get(
    path="/{user_id}/tasks",
    summary="Получение списка задач сотрудника",
    responses={
        200: {
            "model": list[TaskResponseWithProject],
            "description": "Список задач сотрудника получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не является менеджером"
        },
        404: {
            "model": ErrorResponse,
            "description": "Сотрудник не найден"
        }
    }
)
async def get_user_tasks(
        user_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка задач сотрудника"""
    return await ManagerUserService.get_user_tasks(user_id, current_user)


@router.get(
    path="/{user_id}/projects",
    summary="Получение списка проектов сотрудника",
    responses={
        200: {
            "model": list[ProjectResponse],
            "description": "Список проектов сотрудника получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не является менеджером"
        },
        404: {
            "model": ErrorResponse,
            "description": "Сотрудник не найден"
        }
    }
)
async def get_user_projects(
        user_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка проектов сотрудника"""
    return await ManagerUserService.get_user_projects(user_id, current_user)
