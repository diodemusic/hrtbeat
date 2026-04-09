from datetime import datetime
from time import time

import httpx
from sqlalchemy import select

from ..core.notifier import notify_email_users
from ..core.status import Status
from ..models.pings import Ping
from ..models.sites import Site


def ping_sites(session, site_id: int = None):
    if not site_id:
        sites = session.execute(select(Site)).scalars()
    else:
        sites = session.execute(select(Site).where(Site.id == site_id)).scalars()

    for site in sites:
        try:
            start_time = int(time() * 1000)
            r = httpx.get(site.url)
            end_time = int(time() * 1000)
            latency = end_time - start_time
        except httpx.ConnectError:
            pinger_object = Ping(
                site_id=site.id,
                latency=-1,
                status=Status.down,
                timestamp=datetime.now(),
            )
            session.add(pinger_object)

            site.status = Status.down
            site.consecutive_fails += 1

            continue

        pinger_object = Ping(
            site_id=site.id,
            latency=latency,
            timestamp=datetime.now(),
        )
        session.add(pinger_object)

        if r.status_code < 400:
            site.status = Status.healthy
            pinger_object.status = Status.healthy
            site.consecutive_fails = 0
        else:
            site.status = Status.down
            pinger_object.status = Status.down
            site.consecutive_fails += 1

        notify_email_users(session, site_id, site.url, site.consecutive_fails)
