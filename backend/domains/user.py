import pytz
from typing import Optional
from config import settings
from datetime import datetime
from domains.base import DomainBaseModel
from domains.value_objects.email import Email
from domains.value_objects.password import Password


class UserDomain(DomainBaseModel):
    def __init__(
        self,
        id: Optional[int],
        email: str,
        password: str,
        name: str,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id: Optional[int] = id
        self.email: str = email
        self.password: str = password
        self.name: str = name
        self.is_active: bool = is_active
        self.created_at: Optional[datetime] = created_at
        self.updated_at: Optional[datetime] = updated_at

    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now(tz=pytz.timezone(settings.TIMEZONE))  # type: ignore

    @classmethod
    def create(cls, name: str, email: str, password: str) -> "UserDomain":
        """Factory method with business rules"""

        # Validate business rules
        if len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")

        # Create value objects (with their own validation)
        email_vo = Email(email)
        password_vo = Password(password)

        return cls(
            id=None,
            name=name.strip(),
            email=email_vo.__str__(),
            password=password_vo.hash(),
            is_active=True,
            created_at=cls.get_current_time(),
            updated_at=cls.get_current_time(),
        )

    def update_profile(self, name: Optional[str] = None, email: Optional[str] = None):
        """Business method: Update profile with validation"""

        if name is not None:
            if len(name.strip()) < 2:
                raise ValueError("Name must be at least 2 characters")
            self.name = name.strip()

        if email is not None:
            self.email = Email(email).__str__()  # Email validation in value object

    def deactivate(self):
        """Business method: Deactivate user"""
        self.is_active = False

    def can_login(self) -> bool:
        """Business rule: Login eligibility"""
        return self.is_active

    def change_password(self, old_password: str, new_password: str):
        """Business method: Change password with validation"""

        # Verify old password
        if not Password.verify(old_password, self.password):
            raise ValueError("Current password is incorrect")

        # Set new password
        new_password_vo = Password(new_password)
        self.password = new_password_vo.hash()
