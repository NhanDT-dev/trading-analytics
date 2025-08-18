from typing import List
from repositories.user import UserRepository
from schemas.user import UserCreate, UserUpdate, UserInfo


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def add_user(self, user: UserCreate) -> None:
        await self.user_repo.create_item(user)

    async def update_user_profile(self, user: UserUpdate) -> None:
        await self.user_repo.update_item_by_id(user.id, user)

    async def get_all_users(self) -> List[UserInfo]:
        list_users = await self.user_repo.get_list_items()
        return [UserInfo.model_validate(obj=user) for user in list_users]

    async def get_user_by_id(self, user_id: int):
        user = await self.user_repo.get_item_by_id(id=user_id)
        return user
