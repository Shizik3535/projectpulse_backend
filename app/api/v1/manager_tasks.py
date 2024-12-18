from fastapi import APIRouter, Depends, status
from app.core.security import Security

# Сервисы
from app.domains.manager.tasks.services import ManagerTaskService

# Схемы
from app.base.schemas import MessageResponse, ErrorResponse
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.tasks.schemas import (
    TaskResponseWithProject,
    TaskCreate,
    TaskUpdate
)

router = APIRouter(
    prefix="/manager/tasks",
    tags=["Управление задачами"]
)

@router.get(
    path="",
    summary="Получение списка задач",
    responses={
        200: {
            "model": list[TaskResponseWithProject],
            "description": "Список задач получен успешно"
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
async def get_tasks(
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех задач"""
    return await ManagerTaskService.get_tasks(current_user)


@router.get(
    path="/{task_id}",
    summary="Получение задачи",
    responses={
        200: {
            "model": TaskResponseWithProject,
            "description": "Задача получена успешно"
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
            "description": "Задача не найдена"
        }
    }
)
async def get_task(
    task_id: int,
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение задачи по ID"""
    return await ManagerTaskService.get_task(task_id, current_user)


@router.post(
    path="",
    summary="Создание задачи",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": MessageResponse,
            "description": "Задача успешно создана"
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
async def create_task(
    task_data: TaskCreate,
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Создание новой задачи"""
    return await ManagerTaskService.create_task(task_data, current_user)


@router.put(
    path="/{task_id}",
    summary="Обновление задачи",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Задача успешно обновлена"
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
            "description": "Задача не найдена"
        }
    }
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Обновление информации о задаче"""
    return await ManagerTaskService.update_task(task_id, task_data, current_user)


@router.delete(
    path="/{task_id}",
    summary="Удаление задачи",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Задача успешно удалена"
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
            "description": "Задача не найдена"
        }
    }
)
async def delete_task(
    task_id: int,
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Удаление задачи"""
    return await ManagerTaskService.delete_task(task_id, current_user)


@router.get(
    path="/{task_id}/assignments",
    summary="Получение списка сотрудников на задаче",
    responses={
        200: {
            "model": list[UserResponse],
            "description": "Список сотрудников на задаче получен успешно"
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
            "description": "Задача не найдена"
        }
    }
)
async def get_task_assignments(
    task_id: int,
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка сотрудников на задаче"""
    return await ManagerTaskService.get_task_assignments(task_id, current_user)


@router.post(
    path="/{task_id}/assignments",
    summary="Назначение сотрудника на задачу",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": MessageResponse,
            "description": "Сотрудник успешно назначен на задачу"
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
            "description": "Задача или сотрудник не найден"
        }
    }
)
async def add_task_assignment(
    task_id: int,
    user_id: int,
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Назначение сотрудника на задачу"""
    return await ManagerTaskService.add_task_assignment(task_id, user_id, current_user)


@router.delete(
    path="/{task_id}/assignments/{user_id}",
    summary="Удаление сотрудника с задачи",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Сотрудник успешно удален с задачи"
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
            "description": "Задача или сотрудник не найден"
        }
    }
)
async def remove_task_assignment(
    task_id: int,
    user_id: int,
    current_user: UserDB = Depends(Security.get_current_user)
):
    """Удаление сотрудника с задачи"""
    return await ManagerTaskService.remove_task_assignment(task_id, user_id, current_user)
