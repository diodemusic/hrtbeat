from ..models.pings import Ping  # noqa: F401
from ..models.site_watches import SiteWatch  # noqa: F401
from ..models.sites import Site  # noqa: F401
from ..models.users import User  # noqa: F401
from .engine import engine
from .sqlabase import Base


def create_tables():
    Base.metadata.create_all(engine)
