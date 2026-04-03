from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.engine import engine
from ..core.tables import create_tables
from ..models.site_watches import SiteWatch
from ..models.sites import Site

create_tables()


app = FastAPI()


class AddSiteRequest(BaseModel):
    url: str


@app.post("/site", status_code=201)
def add_site(url: AddSiteRequest):
    user_id = 1

    def add_site_watch(session, user_id, site_id) -> dict[str, int]:
        site_watch_object = SiteWatch(user_id=user_id, site_id=site_id)
        session.add(site_watch_object)
        session.flush()

        return {"site_watch": site_watch_object.id}

    with Session(engine) as session:
        stmt = select(Site).where(Site.url == url.url)
        site = session.execute(stmt).scalars().first()

        if site:
            stmt = select(SiteWatch).where(
                SiteWatch.user_id == user_id, SiteWatch.site_id == site.id
            )
            site_watch = session.execute(stmt).scalars().first()

            if site_watch:
                raise HTTPException(
                    status_code=409,
                    detail=f"User {user_id} is already watching site {site.id}: {site_watch}",
                )
            else:
                r = add_site_watch(session=session, user_id=user_id, site_id=site.id)
                session.commit()

                return r
        else:
            site_object = Site(url=url.url)
            session.add(site_object)
            session.flush()
            r = add_site_watch(session=session, user_id=user_id, site_id=site_object.id)
            session.commit()

            return r
