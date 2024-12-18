from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.domains.auth.dao import BlackListTokenDAO
from app.domains.users.dao import UserDAO

from app.domains.users.schemas import UserDB


class Security:
    """
    Класс для работы с безопасностью приложения, включая аутентификацию и авторизацию, токены и т.д.
    """

    # OAuth
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"api/v1/auth/login")
    # Хеширование
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    # Пароль
    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        """Хеширование пароля"""
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return cls.pwd_context.verify(plain_password, hashed_password)

    # JWT
    @classmethod
    def create_token(cls, data: dict) -> str:
        """Создание access токена"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=365)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def verify_and_decode_token(cls, token: str) -> dict:
        """Декодирование токена"""
        try:
            payload = jwt.decode(
                token=token,
                key=settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if payload["exp"] < datetime.now(timezone.utc).timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Срок действия токена истек",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload

    @classmethod
    async def disability_token(cls, token: str) -> None:
        """Добавление токена в BlackList"""
        token_data = cls.verify_and_decode_token(token)
        expires_at = datetime.fromtimestamp(token_data.get("exp"), tz=timezone.utc)
        await BlackListTokenDAO.create(token=token, expires_at=expires_at)

    # Аутентификация
    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> UserDB:
        """Аутентификация пользователя"""
        user = await UserDAO.find_one_or_none(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не верный логин или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not cls.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не верный логин или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)) -> UserDB:
        """Получение текущего пользователя"""
        if await BlackListTokenDAO.find_one_or_none(token=token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не валидиный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload = cls.verify_and_decode_token(token)
        payload["sub"] = int(payload["sub"])
        user = await UserDAO.find_by_id(payload.get("sub"))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    @classmethod
    async def get_role_current_user(cls, user: UserDB = Depends(get_current_user)) -> str:
        """Получение роли текущего пользователя"""
        return user.role.name