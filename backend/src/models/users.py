from sqlalchemy.orm import Mapped, mapped_column

from ..core.sqlabase import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str | None]
    mobile_number: Mapped[str | None]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, mobile_number={self.mobile_number!r})"
