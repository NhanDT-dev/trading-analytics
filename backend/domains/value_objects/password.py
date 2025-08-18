import re
import bcrypt
from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    """Password Value Object with hashing"""

    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[0-9]", self.value):
            raise ValueError("Password must contain number")

    def hash(self) -> str:
        """Hash password for storage"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(self.value.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify(plain_password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed.encode("utf-8"))
