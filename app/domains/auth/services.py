from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Core
from app.core.security import Security

# DAOs
from app.domains.users.dao import UserDAO

# Схемы
from app.domains.auth.schemas import TokenResponse, RegisterRequest
from app.domains.users.schemas import UserDB, UserResponse
from app.base.schemas import ErrorResponse, MessageResponse


class AuthService:
    @staticmethod
    async def login(login_data: OAuth2PasswordRequestForm):
        user = await Security.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не верный логин или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = Security.create_token({
            "sub": str(user.id),
            "role": user.role.name
        })
        return TokenResponse(access_token=token)

    @staticmethod
    async def logout(token: str):
        await Security.disability_token(token)
        return MessageResponse(message="Вы вышли из системы")

    @staticmethod
    async def register(register_data: RegisterRequest):
        if await UserDAO.find_all():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Регистрация невозможна"
            )
        user_id = await UserDAO.create(
            username=register_data.username,
            hashed_password=Security.get_hashed_password(register_data.password),
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            patronymic=register_data.patronymic,
            role_id=2
        )
        token = Security.create_token({
            "sub": str(user_id),
            "role": "Менеджер"
        })
        return TokenResponse(access_token=token)

    @staticmethod
    async def get_me(current_user: UserDB):
        return UserResponse(
            id=current_user.id,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            patronymic=current_user.patronymic,
            role=current_user.role.name,
            position=current_user.position.name if current_user.position else None
        )
