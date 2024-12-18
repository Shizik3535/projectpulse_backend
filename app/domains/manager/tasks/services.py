from fastapi import HTTPException, status

from app.core.security import Security
from app.domains.manager.services import ManagerService

# DAOs
from app.domains.tasks.dao import TaskDAO, TaskAssignmentDAO, TaskPriorityDAO, TaskStatusDAO
from app.domains.projects.dao import ProjectDAO
from app.domains.users.dao import UserDAO

# Схемы
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.projects.schemas import ProjectResponse
from app.domains.tasks.schemas import TaskResponse, TaskResponseWithProject, TaskCreate, TaskUpdate
from app.base.schemas import MessageResponse


class ManagerTaskService(ManagerService):
    @classmethod
    async def get_tasks(
        cls,
        current_user: UserDB,
    ) -> list[TaskResponseWithProject]:
        cls._check_role(current_user.role.name)

        tasks = await TaskDAO.get_tasks_with_project()
        return [
            TaskResponseWithProject(
                id=task.id,
                title=task.title,
                description=task.description,
                start_date=task.start_date,
                due_date=task.due_date,
                priority=task.priority.name,
                status=task.status.name,
                project=ProjectResponse(
                    id=task.project.id,
                    title=task.project.title,
                    description=task.project.description,
                    start_date=task.project.start_date,
                    due_date=task.project.due_date,
                    status=task.project.status.name,
                ) if task.project else None
            ) for task in tasks
        ]

    @classmethod
    async def get_task(
        cls,
        task_id: int,
        current_user: UserDB
    ) -> TaskResponseWithProject:
        cls._check_role(current_user.role.name)
        task = await TaskDAO.get_task_with_project(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        return TaskResponseWithProject(
            id=task.id,
            title=task.title,
            description=task.description,
            start_date=task.start_date,
            due_date=task.due_date,
            priority=task.priority.name,
            status=task.status.name,
            project=ProjectResponse(
                id=task.project.id,
                title=task.project.title,
                description=task.project.description,
                start_date=task.project.start_date,
                due_date=task.project.due_date,
                status=task.project.status.name,
            ) if task.project else None
        )

    @classmethod
    async def create_task(
        cls,
        task: TaskCreate,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        await TaskDAO.create(
            title=task.title,
            description=task.description,
            start_date=task.start_date,
            due_date=task.due_date
        )
        return MessageResponse(
            message="Задача успешно создана"
        )

    @classmethod
    async def update_task(
        cls,
        task_id: int,
        task: TaskUpdate,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        if not await TaskPriorityDAO.find_by_id(task.priority_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Приоритет задачи не найден"
            )
        if not await TaskStatusDAO.find_by_id(task.status_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Статус задачи не найден"
            )
        if task.project_id and not await ProjectDAO.find_by_id(task.project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )
        await TaskDAO.update(
            model_id=task_id,
            title=task.title,
            description=task.description,
            start_date=task.start_date,
            due_date=task.due_date,
            priority_id=task.priority_id,
            status_id=task.status_id,
            project_id=task.project_id,
        )
        return MessageResponse(
            message="Задача успешно обновлена"
        )
    
    @classmethod
    async def delete_task(
        cls,
        task_id: int,
        current_user: UserDB
    ) -> MessageResponse:
        cls._check_role(current_user.role.name)
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        await TaskDAO.delete(model_id=task_id)
        return MessageResponse(
            message="Задача успешно удалена"
        )
    
    @classmethod
    async def get_task_assignments(
        cls,
        task_id: int,
        current_user: UserDB
    ):
        cls._check_role(current_user.role.name)
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        users = await TaskAssignmentDAO.get_task_assignments(task_id)
        return [
            UserResponse(
                id=user.user.id,
                first_name=user.user.first_name,
                last_name=user.user.last_name,
                patronymic=user.user.patronymic,
                role=user.user.role.name,
                position=user.user.position.name if user.user.position else None
            ) for user in users
        ]

    @classmethod
    async def add_task_assignment(
        cls,
        task_id: int,
        user_id: int,
        current_user: UserDB
    ):
        cls._check_role(current_user.role.name)
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        await TaskAssignmentDAO.create(
            task_id=task_id,
            user_id=user_id
        )
        return MessageResponse(
            message="Пользователь успешно назначен на задачу"
        )

    @classmethod
    async def remove_task_assignment(
        cls,
        task_id: int,
        user_id: int,
        current_user: UserDB
    ):
        cls._check_role(current_user.role.name)
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        if not await UserDAO.find_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        if not await TaskAssignmentDAO.find_one_or_none(
            task_id=task_id,
            user_id=user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не назначен на задачу"
            )
        await TaskAssignmentDAO.delete_by_filter(
            task_id=task_id,
            user_id=user_id
        )
        return MessageResponse(
            message="Пользователь успешно удален из задачи"
        )
