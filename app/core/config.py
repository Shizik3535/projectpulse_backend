from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # База данных
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str

    # Сервер
    SERVER_HOST: str
    SERVER_PORT: int

    class Config:
        # Настройки для .env
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
