from typing import (
    Union,
    Optional,
    Generic,
    TypeVar,
    Dict,
    Any,
    Type,
    Sequence,
)
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from database.model import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateModelType = TypeVar("CreateModelType", bound=BaseModel)
UpdateModelType = TypeVar("UpdateModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateModelType, UpdateModelType]):
    def __init__(self, model_type: Type[ModelType], db_session: AsyncSession) -> None:
        self.model = model_type
        self.db_session = db_session

    async def create_item(self, obj_in: CreateModelType) -> None:
        """Create new item and return created instance"""
        data = obj_in.model_dump()
        db_obj = self.model(**data)
        await self.save(db_obj)

    async def get_list_items(self, *fields, **filters) -> Sequence[tuple]:
        """Get filtered list of items"""
        if fields:
            stmt = select(*fields)
        else:
            stmt = select(self.model)

        stmt = stmt.where(**filters)  # type: ignore
        result = await self.db_session.execute(stmt)
        return result.fetchall()

    async def get_item_by_id(
        self, id: Union[str, int], *fields, **filters
    ) -> Optional[ModelType]:
        """Get single item by ID, return None if not found"""
        if fields:
            stmt = select(*fields)
        else:
            stmt = select(self.model)

        stmt = stmt.where(self.model.id == id, **filters)  # type: ignore
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_paginated_items(
        self, limit: int = 10, offset: int = 0, **filters
    ) -> Dict[str, Any]:  # hoặc PaginationResult model
        """Get paginated items with metadata"""
        ...

    async def update_item_by_id(
        self, id: Union[str, int], update_data: UpdateModelType
    ) -> None:
        """Update item and return updated instance"""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db_session.execute(stmt)
        entity_obj = result.scalar_one_or_none()

        if not entity_obj:
            return
        update_model = self.model(**update_data.model_dump())
        await self.save(update_model)

    async def delete_item_by_id(self, id: Union[str, int]) -> bool:
        """Delete item and return success status"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount > 0

    async def save(self, entity_obj: ModelType) -> None:
        """Save item and return created instance"""
        self.db_session.add(entity_obj)
        await self.db_session.commit()
        await self.db_session.refresh(entity_obj)
