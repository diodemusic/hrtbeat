from datetime import datetime
from time import sleep, time

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.engine import engine
from ..models.pings import Ping
from ..models.sites import Site, Status

while True:
    with Session(engine) as session:
        stmt = select(Site)
        sites = session.execute(stmt).scalars()

        for site in sites:
            try:
                start_time = int(time() * 1000)
                r = httpx.get(site.url)
                end_time = int(time() * 1000)
                latency = end_time - start_time
            except httpx.ConnectError:
                pinger_object = Ping(
                    site_id=site.id, latency=-1, timestamp=datetime.now()
                )
                session.add(pinger_object)

                site.status = Status.down
                site.consecutive_fails += 1
                session.commit()

                continue

            pinger_object = Ping(
                site_id=site.id, latency=latency, timestamp=datetime.now()
            )
            session.add(pinger_object)

            if r.status_code < 400:
                site.status = Status.healthy
                site.consecutive_fails = 0
            else:
                site.status = Status.down
                site.consecutive_fails += 1

            session.commit()

    sleep(60 * 5)
