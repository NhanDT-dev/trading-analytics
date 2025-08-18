from typing import Annotated
from database.session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from services.user import UserService
from repositories.user import UserRepository


def get_user_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return UserRepository(session)


def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(user_repo)
