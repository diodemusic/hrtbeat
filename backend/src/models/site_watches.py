from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..core.sqlabase import Base


class SiteWatch(Base):
    __tablename__ = "site_watches"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    notify_email: Mapped[bool] = False
    notify_mobile: Mapped[bool] = False

    def __repr__(self) -> str:
        return f"SiteWatch(id={self.id!r}, user_id={self.user_id!r}, site_id={self.site_id!r}, notify_email={self.notify_email!r}, notify_mobile={self.notify_mobile!r})"
