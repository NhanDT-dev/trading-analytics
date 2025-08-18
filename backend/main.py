from typing import Annotated, Optional, Union
from fastapi import FastAPI, Depends
from database.session import async_session, get_db_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.common import User

app = FastAPI(title="Trading analytics API")


@app.get("/")
async def test(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    stmt = select(User.id, User.name, User.email)
    result = await db_session.execute(stmt)
    data = result.fetchone()
    print("data", data)
    return data
