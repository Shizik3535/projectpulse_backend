from fastapi import APIRouter, Depends
from app.core.security import Security

# Сервисы
from app.domains.manager.reports.services import ReportsService

# Схемы
from app.base.schemas import ErrorResponse
from app.domains.users.schemas import UserDB

router = APIRouter(
    prefix="/manager/reports",
    tags=["Управление отчётами"]
)


@router.get(
    path="/tasks/{task_id}",
    summary="Создание отчёта по задаче",
    responses={
        200: {
            "model": None,
            "description": "Отчёт скачан успешно",
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
        },
    },
)
async def create_report_by_task(
        task_id: int,
        current_user: UserDB = Depends(Security.get_current_user),
):
    """Создание отчёта по задаче"""
    return await ReportsService.create_report_by_task(task_id, current_user)


@router.get(
    path="/projects/{project_id}",
    summary="Создание отчёта по проекту",
    responses={
        200: {
            "model": None,
            "description": "Отчёт скачан успешно",
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
            "description": "Проект не найден"
        },
    }
)
async def create_report_by_project(
        project_id: int,
        current_user: UserDB = Depends(Security.get_current_user),
):
    """Создание отчёта по проекту"""
    return await ReportsService.create_report_by_project(project_id, current_user)


@router.get(
    path="/users/{user_id}",
    summary="Создание отчёта по пользователю",
    responses={
        200: {
            "model": None,
            "description": "Отчёт скачан успешно",
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
            "description": "Пользователь не найден"
        },
    }
)
async def create_report_by_user(
        user_id: int,
        current_user: UserDB = Depends(Security.get_current_user),
):
    """Создание отчёта по пользователю"""
    return await ReportsService.create_report_by_user(user_id, current_user)
