from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.engine import engine
from ..core.tables import create_tables
from ..models.site_watches import SiteWatch
from ..models.sites import Site

USER_ID = 1

create_tables()


app = FastAPI()


class AddSiteRequest(BaseModel):
    url: str


class DeleteSiteRequest(BaseModel):
    id: int


@app.post("/site", status_code=201)
def add_site(addSiteRequest: AddSiteRequest):
    def add_site_watch(session, user_id, site_id) -> dict[str, int]:
        site_watch_object = SiteWatch(user_id=user_id, site_id=site_id)
        session.add(site_watch_object)
        session.flush()

        return {"site_watch": site_watch_object.id}

    with Session(engine) as session:
        stmt = select(Site).where(Site.url == addSiteRequest.url)
        site = session.execute(stmt).scalars().first()

        if site:
            stmt = select(SiteWatch).where(
                SiteWatch.user_id == USER_ID, SiteWatch.site_id == site.id
            )
            site_watch = session.execute(stmt).scalars().first()

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
            site_object = Site(url=addSiteRequest.url)
            session.add(site_object)
            session.flush()
            r = add_site_watch(session=session, user_id=USER_ID, site_id=site_object.id)
            session.commit()

            return r


@app.delete("/site-watch", status_code=204)
def delete_site_watch(deleteSiteRequest: DeleteSiteRequest):
    with Session(engine) as session:
        stmt = select(SiteWatch).where(
            SiteWatch.id == deleteSiteRequest.id, SiteWatch.user_id == USER_ID
        )
        site_watch = session.execute(stmt).scalars().first()

        if not site_watch:
            raise HTTPException(
                status_code=404,
                detail=f"Not found: {site_watch}",
            )

        session.delete(site_watch)
        session.flush()

        stmt = select(SiteWatch).where(SiteWatch.site_id == site_watch.site_id)
        other_site_watch = session.execute(stmt).scalars().first()

        if not other_site_watch:
            stmt = select(Site).where(Site.id == site_watch.site_id)
            site = session.execute(stmt).scalars().first()

            session.delete(site)

        session.commit()


@app.get("/site-watches", status_code=200)
def get_site_watches():
    with Session(engine) as session:
        stmt = select(SiteWatch).where(SiteWatch.user_id == USER_ID)
        site_watches = session.execute(stmt).scalars()

        response = []

        for site_watch in site_watches:
            stmt = select(Site).where(Site.id == site_watch.site_id)
            site = session.execute(stmt).scalars().first()
            response.append(
                {
                    "url": site.url,
                    "status": site.status,
                    "pings": [
                        {"latency": 20, "timestamp": "2026-04-04T12:00:00"},
                        {"latency": 35, "timestamp": "2026-04-04T12:05:00"},
                    ],
                }
            )

        return response
