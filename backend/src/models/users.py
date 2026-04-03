from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ..core.sqlabase import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[Optional[str]]
    mobile_number: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, mobile_number={self.mobile_number!r})"
