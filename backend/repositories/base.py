from typing import Union, Optional, List, Generic, TypeVar, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)  # Hoặc có thể bound với SQLAlchemy Base


class BaseRepository(Generic[T], ABC):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    @abstractmethod
    async def create_item(self, item_data: Dict[str, Any]) -> T:
        """Create new item and return created instance"""
        pass

    @abstractmethod
    async def get_list_items(self, **filters) -> List[T]:
        """Get filtered list of items"""
        pass

    @abstractmethod
    async def get_item_by_id(self, id: Union[str, int]) -> Optional[T]:
        """Get single item by ID, return None if not found"""
        pass

    @abstractmethod
    async def get_paginated_items(
        self, limit: int = 10, offset: int = 0, **filters
    ) -> Dict[str, Any]:  # hoặc PaginationResult model
        """Get paginated items with metadata"""
        pass

    @abstractmethod
    async def update_item_by_id(
        self, id: Union[str, int], update_data: Dict[str, Any]
    ) -> Optional[T]:
        """Update item and return updated instance"""
        pass

    @abstractmethod
    async def delete_item_by_id(self, id: Union[str, int]) -> bool:
        """Delete item and return success status"""
        pass
