from pydantic import BaseModel
from datetime import date


class StatusResponse(BaseModel):
    id: int
    name: str


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str | None
    start_date: date | None
    due_date: date | None
    status: str


class ProjectCreate(BaseModel):
    title: str
    description: str | None
    start_date: date | None
    due_date: date | None


class ProjectUpdate(BaseModel):
    title: str
    description: str | None
    start_date: date | None
    due_date: date | None
    status_id: int
