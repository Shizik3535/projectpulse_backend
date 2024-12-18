from pydantic import BaseModel
from datetime import datetime


class RoleResponse(BaseModel):
    id: int
    name: str


class PositionResponse(BaseModel):
    id: int
    name: str


class UserDB(BaseModel):
    id: int
    username: str
    hashed_password: str
    first_name: str
    last_name: str
    patronymic: str | None
    position_id: int | None
    role_id: int
    role: RoleResponse
    position: PositionResponse | None

    created_at: datetime
    updated_at: datetime


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None
    role: str
    position: str | None


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    patronymic: str | None
    position_id: int | None = None


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    position_id: int | None = None
    role_id: int = 1

