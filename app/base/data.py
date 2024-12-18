from app.domains.users.dao import RoleDAO, PositionDAO
from app.domains.tasks.dao import TaskPriorityDAO, TaskStatusDAO
from app.domains.projects.dao import ProjectStatusDAO


async def init_data():
    async def init_data_for_role():
        roles = [
            {"name": "Сотрудник"},
            {"name": "Менеджер"},
        ]

        for role in roles:
            await RoleDAO.create(**role)

    async def init_data_for_position():
        positions = [
            {"name": "Директор"},
            {"name": "Менеджер"},
            {"name": "Сотрудник"},
            {"name": "Инженер"},
            {"name": "Программист"},
            {"name": "Тестировщик"},
            {"name": "Дизайнер"},
            {"name": "Бухгалтер"},
        ]

        for position in positions:
            await PositionDAO.create(**position)
        
    async def init_data_for_task_priority():
        priorities = [
            {"name": "Низкий"},
            {"name": "Средний"},
            {"name": "Высокий"},
        ]

        for priority in priorities:
            await TaskPriorityDAO.create(**priority)

    async def init_data_for_task_status():
        statuses = [
            {"name": "Новая"},
            {"name": "В работе"},
            {"name": "Завершена"},
        ]

        for status in statuses:
            await TaskStatusDAO.create(**status)

    async def init_data_for_project_status():
        statuses = [
            {"name": "Новый"},
            {"name": "В работе"},
            {"name": "Завершен"},
        ]

        for status in statuses:
            await ProjectStatusDAO.create(**status)

    await init_data_for_role()
    await init_data_for_position()
    await init_data_for_task_priority()
    await init_data_for_task_status()
    await init_data_for_project_status()


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_data())