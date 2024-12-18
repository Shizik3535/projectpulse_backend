from fastapi import APIRouter, Depends

from app.core.security import Security
from app.domains.tasks.services import TaskService
# Схемы
from app.base.schemas import MessageResponse, ErrorResponse
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.tasks.schemas import TaskResponseWithProject


router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


@router.get(
    path="/",
    summary="Получение задач",
    responses={
        200: {
            "model": list[TaskResponseWithProject],
            "description": "Список задач получен успешно"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_user_tasks(
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка задач текущего пользователя"""
    return await TaskService.get_user_tasks(current_user)


@router.get(
    path="/{task_id}",
    summary="Получение конкретной задачи",
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
            "description": "Пользователь не участвует в задаче или в проекте, в которой задача"
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
    """Получение конкретной задачи"""
    return await TaskService.get_task(task_id, current_user)


@router.get(
    path="/{task_id}/assignments",
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
            "description": "Пользователь не участвует в задаче или в проекте, в которой задача"
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
    """Получение списка сотрудников, назначенных на конкретную задачу"""
    return await TaskService.get_task_assignments(task_id, current_user)


@router.put(
    path="/{task_id}/status",
    summary="Изменение статуса задачи",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Статус задачи изменен успешно"
        },
        400: {
            "model": ErrorResponse,
            "description": "Статуса не существует"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        },
        403: {
            "model": ErrorResponse,
            "description": "Пользователь не участвует в задаче"
        },
        404: {
            "model": ErrorResponse,
            "description": "Задача не найдена"
        }
    }
)
async def change_task_status(
        task_id: int,
        status_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Изменение статуса задачи"""
    return await TaskService.change_task_status(task_id, status_id, current_user)
