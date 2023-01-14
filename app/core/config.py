from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд QRKot'
    app_description: str = 'Фонд поддержки котиков QRKot.'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()