from repositories.base import BaseRepository
from models.common import User
from schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
