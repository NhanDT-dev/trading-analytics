from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from database.engine import async_engine

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
