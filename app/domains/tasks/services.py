from fastapi import HTTPException, status

# DAOs
from app.domains.tasks.dao import TaskStatusDAO, TaskPriorityDAO, TaskAssignmentDAO, TaskDAO

# Схемы
from app.domains.users.schemas import UserDB, UserResponse
from app.domains.tasks.schemas import TaskResponseWithProject
from app.domains.projects.schemas import ProjectResponse
from app.base.schemas import MessageResponse


class TaskService:
    @classmethod
    async def get_all_statuses(cls):
        return await TaskStatusDAO.find_all()

    @classmethod
    async def get_all_priorities(cls):
        return await TaskPriorityDAO.find_all()

    @classmethod
    async def get_user_tasks(cls, current_user: UserDB):
        tasks = await TaskAssignmentDAO.get_user_tasks(user_id=current_user.id)
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
    async def get_task(cls, task_id: int, current_user: UserDB):
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        if not await TaskAssignmentDAO.find_one_or_none(task_id=task_id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не являетесь участником задачи"
            )
        task = await TaskDAO.get_task_with_project(task_id)
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
    async def get_task_assignments(cls, task_id: int, current_user: UserDB):
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        if not await TaskAssignmentDAO.find_one_or_none(task_id=task_id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не являетесь участником задачи"
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
    async def change_task_status(cls, task_id: int, status_id: int, current_user: UserDB):
        if not await TaskDAO.find_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Задача не найдена"
            )
        if not await TaskAssignmentDAO.find_one_or_none(task_id=task_id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не являетесь участником задачи"
            )
        if not await TaskStatusDAO.find_by_id(status_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Статус не найден"
            )
        await TaskDAO.update(model_id=task_id, status_id=status_id)
        return MessageResponse(message="Статус задачи успешно изменен")
        