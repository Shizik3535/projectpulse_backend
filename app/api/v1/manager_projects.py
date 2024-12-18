from fastapi import APIRouter, Depends, status
from app.core.security import Security

# Сервисы
from app.domains.manager.projects.services import ManagerProjectService

# Схемы
from app.base.schemas import MessageResponse, ErrorResponse
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.tasks.schemas import TaskResponse
from app.domains.projects.schemas import (
    ProjectResponse,
    ProjectCreate,
    ProjectUpdate
)

router = APIRouter(
    prefix="/manager/projects",
    tags=["Управление проектами"]
)


@router.get(
    path="",
    summary="Получение списка проектов",
    responses={
        200: {
            "model": list[ProjectResponse],
            "description": "Список проектов получен успешно"
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
async def get_projects(
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка всех проектов"""
    return await ManagerProjectService.get_projects(current_user)


@router.get(
    path="/{project_id}",
    summary="Получение проекта",
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
            "description": "Пользователь не является менеджером"
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
    """Получение проекта по ID"""
    return await ManagerProjectService.get_project(project_id, current_user)


@router.post(
    path="",
    summary="Создание проекта",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": MessageResponse,
            "description": "Проект успешно создан"
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
async def create_project(
        project_data: ProjectCreate,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Создание нового проекта"""
    return await ManagerProjectService.create_project(project_data, current_user)


@router.put(
    path="/{project_id}",
    summary="Обновление проекта",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Проект успешно обновлен"
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
            "description": "Проект или статус не найден"
        }
    }
)
async def update_project(
        project_id: int,
        project_data: ProjectUpdate,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Обновление информации о проекте"""
    return await ManagerProjectService.update_project(project_id, project_data, current_user)


@router.delete(
    path="/{project_id}",
    summary="Удаление проекта",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Проект успешно удален"
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
        }
    }
)
async def delete_project(
        project_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Удаление проекта"""
    return await ManagerProjectService.delete_project(project_id, current_user)


# Назначение и удаление сотрудников на проекте
@router.get(
    path="/{project_id}/members",
    summary="Получение списка сотрудников на проекте",
    responses={
        200: {
            "model": list[UserResponse],
            "description": "Список сотрудников на проекте получен успешно"
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
        }
    }
)
async def get_project_members(
        project_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка сотрудников на проекте"""
    return await ManagerProjectService.get_project_members(project_id, current_user)


@router.post(
    path="/{project_id}/members",
    summary="Назначение сотрудника на проект",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": MessageResponse,
            "description": "Сотрудник успешно назначен на проект"
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
            "description": "Проект или сотрудник не найден"
        }
    }
)
async def add_project_member(
        project_id: int,
        user_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Назначение сотрудника на проект"""
    return await ManagerProjectService.add_project_member(project_id, user_id, current_user)


@router.delete(
    path="/{project_id}/members/{user_id}",
    summary="Удаление сотрудника с проекта",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Сотрудник успешно удален с проекта"
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
            "description": "Проект или сотрудник не найден"
        }
    }
)
async def remove_project_member(
        project_id: int,
        user_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Удаление сотрудника с проекта"""
    return await ManagerProjectService.remove_project_member(project_id, user_id, current_user)


@router.get(
    path="/{project_id}/tasks",
    summary="Получение списка задач на проекте",
    responses={
        200: {
            "model": list[TaskResponse],
            "description": "Список задач на проекте получен успешно"
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
        }
    }
)
async def get_project_tasks(
        project_id: int,
        current_user: UserDB = Depends(Security.get_current_user)
):
    """Получение списка задач на проекте"""
    return await ManagerProjectService.get_project_tasks(project_id, current_user)