from .auth import router as auth_router
from .reference import router as reference_router
from .tasks import router as tasks_router
from .projects import router as projects_router
from .manager_projects import router as manager_projects_router
from .manager_tasks import router as manager_tasks_router
from .manager_users import router as manager_users_router
from .manager_reports import router as manager_reports_router


routers = [
    auth_router,
    reference_router,
    tasks_router,
    projects_router,
    manager_users_router,
    manager_projects_router,
    manager_tasks_router,
    manager_reports_router
]