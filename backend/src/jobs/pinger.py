from datetime import datetime, timedelta
from time import sleep

from sqlalchemy import delete
from sqlalchemy.orm import Session

from ..core.engine import engine
from ..core.ping import ping_sites
from ..models.pings import Ping

while True:
    with Session(engine) as session:
        ping_sites(session)

        session.execute(
            delete(Ping).where(Ping.timestamp < datetime.now() - timedelta(days=7))
        )

        session.commit()

    sleep(60 * 5)
