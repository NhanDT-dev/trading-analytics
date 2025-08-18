from typing import Annotated, Optional, Union
from fastapi import FastAPI, Depends
from services.user import UserService
from core.dependencies import get_user_service
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.common import User

app = FastAPI(title="Trading analytics API")


@app.get("/")
async def test(user_service: Annotated[UserService, Depends(get_user_service)]):
    data = await user_service.get_all_users()
    print("data", data)
    return data
