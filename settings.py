import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')
    DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'root')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@' \
               f'{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'


settings = Settings()