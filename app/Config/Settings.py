from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Clean Modular"
    debug: bool = False

    database_url: str
    jwt_secret: str
    jwt_expire_minutes: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
