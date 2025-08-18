from datetime import datetime
from database.model import Base
from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from config import settings
import pytz


class Model:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), default=datetime.now(tz=pytz.timezone(settings.TIMEZONE)) # type: ignore
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(True))


class User(Base, Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
