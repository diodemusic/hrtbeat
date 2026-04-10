import socket
from typing import Annotated, Optional, Union

import phonenumbers
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BeforeValidator, EmailStr, HttpUrl
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from ..core.engine import engine
from ..core.ping import ping_sites
from ..core.tables import create_tables
from ..models.pings import Ping
from ..models.site_watches import SiteWatch
from ..models.sites import Site
from ..models.users import User

USER_ID = 1

create_tables()


app = FastAPI()


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def prepend_scheme(url: str):
    if "://" not in url:
        url = f"https://{url}"

    return url


class AddSiteRequest(BaseModel):
    url: Annotated[HttpUrl, BeforeValidator(prepend_scheme)]


class DeleteSiteRequest(BaseModel):
    id: int


MyNumberType = Annotated[Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator()]


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    mobile_number: Optional[MyNumberType] = None


class UserSiteWatchNotificationsRequest(BaseModel):
    site_id: int
    notify_email: Optional[bool] = None
    notify_mobile: Optional[bool] = None


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
        try:
            site_watch = session.execute(
                select(SiteWatch).where(
                    SiteWatch.id == deleteSiteRequest.id,
                    SiteWatch.user_id == USER_ID,
                )
            ).scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail=f"Not found: site_watch {deleteSiteRequest.id}",
            )

        session.delete(site_watch)
        session.flush()

        other_site_watch = (
            session.execute(
                select(SiteWatch)
                .where(SiteWatch.site_id == site_watch.site_id)
                .limit(1)
            )
            .scalars()
            .first()
        )

        if not other_site_watch:
            site = session.execute(
                select(Site).where(Site.id == site_watch.site_id)
            ).scalar_one()

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
            site = session.execute(
                select(Site).where(Site.id == site_watch.site_id)
            ).scalar_one()
            pings = session.execute(
                select(Ping)
                .where(Ping.site_id == site.id)
                .order_by(Ping.id.desc())
                .limit(100)
            ).scalars()

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


@app.put("/user", status_code=200)
def update_user(userUpdateRequest: UserUpdateRequest):
    with Session(engine) as session:
        try:
            user = session.execute(select(User).where(User.id == USER_ID)).scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail=f"Not found: {USER_ID}",
            )

        if "email" in userUpdateRequest.model_fields_set:
            user.email = userUpdateRequest.email

            if not userUpdateRequest.email:
                site_watches = session.execute(
                    select(SiteWatch).where(SiteWatch.user_id == USER_ID)
                ).scalars()

                for site_watch in site_watches:
                    site_watch.notify_email = False

        if "mobile_number" in userUpdateRequest.model_fields_set:
            user.mobile_number = userUpdateRequest.mobile_number

        r = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "mobile_number": user.mobile_number,
        }

        session.commit()

    return r


@app.put("/site-watches", status_code=200)
def update_site_watch_notifications(
    userSiteWatchNotificationsRequest: UserSiteWatchNotificationsRequest,
):
    with Session(engine) as session:
        try:
            user = session.execute(select(User).where(User.id == USER_ID)).scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail=f"Not found: user {USER_ID}",
            )

        if (
            "notify_email" in userSiteWatchNotificationsRequest.model_fields_set
            and not user.email
        ) or (
            "notify_mobile" in userSiteWatchNotificationsRequest.model_fields_set
            and not user.mobile_number
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Not found: {user}",
            )

        try:
            site_watch = session.execute(
                select(SiteWatch).where(
                    SiteWatch.user_id == USER_ID,
                    SiteWatch.site_id == userSiteWatchNotificationsRequest.site_id,
                )
            ).scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail=f"Not found: site_id {userSiteWatchNotificationsRequest.site_id}",
            )

        if "notify_email" in userSiteWatchNotificationsRequest.model_fields_set:
            site_watch.notify_email = userSiteWatchNotificationsRequest.notify_email

        if "notify_mobile" in userSiteWatchNotificationsRequest.model_fields_set:
            site_watch.notify_mobile = userSiteWatchNotificationsRequest.notify_mobile

        r = {
            "id": site_watch.id,
            "user_id": site_watch.user_id,
            "site_id": site_watch.site_id,
            "notify_email": site_watch.notify_email,
            "notify_mobile": site_watch.notify_mobile,
        }

        session.commit()

    return r
