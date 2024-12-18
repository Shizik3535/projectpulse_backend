from pydantic import BaseModel


# Ответы
class TokenResponse(BaseModel):
    """Схема ответа для токена аутентификации"""
    access_token: str
    token_type: str = "bearer"


# Запросы
class RegisterRequest(BaseModel):
    """Схема запроса на регистрацию"""
    username: str
    password: str
    first_name: str
    last_name: str
    patronymic: str | None
