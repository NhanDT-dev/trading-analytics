from sqlalchemy.ext.asyncio import create_async_engine
from config import settings

async_engine = create_async_engine(
    url=f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}",
    echo=True,
)
