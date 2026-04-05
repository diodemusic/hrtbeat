import socket
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, BeforeValidator, HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.engine import engine
from ..core.ping import ping_sites
from ..core.tables import create_tables
from ..models.pings import Ping
from ..models.site_watches import SiteWatch
from ..models.sites import Site

USER_ID = 1

create_tables()


app = FastAPI()


def prepend_scheme(url: str):
    if "://" not in url:
        url = f"https://{url}"

    return url


class AddSiteRequest(BaseModel):
    url: Annotated[HttpUrl, BeforeValidator(prepend_scheme)]


class DeleteSiteRequest(BaseModel):
    id: int


@app.post("/site-watch", status_code=201)
def add_site(addSiteRequest: AddSiteRequest):
    def add_site_watch(session, user_id, site_id):
        site_watch_object = SiteWatch(user_id=user_id, site_id=site_id)
        session.add(site_watch_object)
        session.flush()

        return {"site_watch": site_watch_object.id}

    try:
        r = socket.getaddrinfo(addSiteRequest.url.host, 0)
    except socket.gaierror:
        raise HTTPException(
            status_code=400, detail=f"Bad Request: {addSiteRequest.url}"
        )

    with Session(engine) as session:
        site = (
            session.execute(select(Site).where(Site.url == str(addSiteRequest.url)))
            .scalars()
            .first()
        )

        if site:
            site_watch = (
                session.execute(
                    select(SiteWatch).where(
                        SiteWatch.user_id == USER_ID, SiteWatch.site_id == site.id
                    )
                )
                .scalars()
                .first()
            )

            if site_watch:
                raise HTTPException(
                    status_code=409,
                    detail=f"Conflict: {site_watch}",
                )
            else:
                r = add_site_watch(session=session, user_id=USER_ID, site_id=site.id)
                session.commit()

                return r
        else:
            site_object = Site(url=str(addSiteRequest.url))
            session.add(site_object)
            session.flush()
            r = add_site_watch(session=session, user_id=USER_ID, site_id=site_object.id)
            session.flush()
            ping_sites(session, site_object.id)
            session.commit()

            return r


@app.delete("/site-watch", status_code=204)
def delete_site_watch(deleteSiteRequest: DeleteSiteRequest):
    with Session(engine) as session:
        site_watch = (
            session.execute(
                select(SiteWatch).where(
                    SiteWatch.id == deleteSiteRequest.id, SiteWatch.user_id == USER_ID
                )
            )
            .scalars()
            .first()
        )

        if not site_watch:
            raise HTTPException(
                status_code=404,
                detail=f"Not found: {site_watch}",
            )

        session.delete(site_watch)
        session.flush()

        other_site_watch = (
            session.execute(
                select(SiteWatch).where(SiteWatch.site_id == site_watch.site_id)
            )
            .scalars()
            .first()
        )

        if not other_site_watch:
            site = (
                session.execute(select(Site).where(Site.id == site_watch.site_id))
                .scalars()
                .first()
            )

            session.delete(site)

        session.commit()


@app.get("/site-watches", status_code=200)
def get_site_watches():
    with Session(engine) as session:
        site_watches = session.execute(
            select(SiteWatch).where(SiteWatch.user_id == USER_ID)
        ).scalars()

        response = []

        for site_watch in site_watches:
            site = (
                session.execute(select(Site).where(Site.id == site_watch.site_id))
                .scalars()
                .first()
            )
            pings = (
                session.execute(
                    select(Ping)
                    .where(Ping.site_id == site.id)
                    .order_by(Ping.id.desc())
                    .limit(100)
                )
                .scalars()
                .all()
            )

            response.append(
                {
                    "url": site.url,
                    "status": site.status,
                    "pings": [
                        {
                            "latency": ping.latency,
                            "status": ping.status,
                            "timestamp": ping.timestamp,
                        }
                        for ping in pings
                    ],
                }
            )

        return response
