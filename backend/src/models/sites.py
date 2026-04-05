from sqlalchemy.orm import Mapped, mapped_column

from ..core.sqlabase import Base
from ..core.status import Status


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True)
    status: Mapped[Status] = mapped_column(default=Status.healthy)
    consecutive_fails: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"Site(id={self.id!r}, url={self.url!r}, status={self.status!r}, consecutive_fails={self.consecutive_fails!r})"
