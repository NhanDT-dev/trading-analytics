from sqlalchemy.ext.asyncio.session import async_sessionmaker
from database.engine import async_engine

session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
