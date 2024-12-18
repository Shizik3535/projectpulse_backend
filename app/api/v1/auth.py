from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import Security
from app.domains.auth.services import AuthService
# Схемы
from app.domains.auth.schemas import (
    TokenResponse,
    RegisterRequest,
)
from app.domains.users.schemas import UserResponse, UserDB
from app.base.schemas import MessageResponse, ErrorResponse

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post(
    path="/login",
    summary="Вход в систему",
    responses={
        200: {
            "model": TokenResponse,
            "description": "Токен авторизации"
        },
        401: {
            "model": ErrorResponse,
            "description": "Неверный логин или пароль"
        }
    }
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends()
) -> TokenResponse:
    """
    Аутентификация пользователя с возвратом токена и информации о пользователе
    """
    return await AuthService.login(login_data=form_data)


@router.post(
    path="/logout", 
    summary="Выход из системы",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Успешный выход из системы"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def logout(
        token: str = Depends(Security.oauth2_scheme)
) -> MessageResponse:
    """
    Выход из системы с инвалидацией токена
    """
    return await AuthService.logout(token=token)


@router.post(
    path="/register",
    summary="Регистрация первого пользователя",
    responses={
        201: {
            "model": TokenResponse,
            "description": "Успешная регистрация пользователя"
        },
        400: {
            "model": ErrorResponse,
            "description": "Регистрация невозможна"
        },
    }
)
async def register(
        register_data: RegisterRequest
) -> TokenResponse:
    """
    Регистрация первого пользователя, если в системе не существует ни одного пользователя
    """
    return await AuthService.register(register_data=register_data)


@router.get(
    path="/me",
    summary="Получение информации о текущем пользователе",
    responses={
        200: {
            "model": UserResponse,
            "description": "Информация о текущем пользователе"
        },
        401: {
            "model": ErrorResponse,
            "description": "Токен авторизации неверен или истек"
        }
    }
)
async def get_me(
        current_user: UserDB = Depends(Security.get_current_user)
) -> UserResponse:
    """
    Получение детальной информации о текущем авторизованном пользователе
    """
    return await AuthService.get_me(current_user=current_user)
