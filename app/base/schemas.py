from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Ответ с сообщением"""
    message: str = "Инофрмация о успешной операции"


class ErrorResponse(BaseModel):
    """Ответ с ошибкой"""
    detail: str = "Информация об ошибке"
