from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..core.sqlabase import Base
from ..models.sites import Status


class Ping(Base):
    __tablename__ = "pings"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    latency: Mapped[int | None]
    status: Mapped[Status]
    timestamp: Mapped[datetime]

    def __repr__(self) -> str:
        return f"Ping(id={self.id!r}, site_id={self.site_id!r}, latency={self.latency!r}, timestamp={self.timestamp!r})"
