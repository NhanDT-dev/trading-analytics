from database.model import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    email: Mapped[str] = mapped_column(
        "email",
    )
