from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/forum_system_db?charset=utf8mb4"
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    APP_NAME: str = "智投社区"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
