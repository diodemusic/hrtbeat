import boto3
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from ..models.site_watches import SiteWatch
from ..models.users import User

client = boto3.client("ses", region_name="eu-west-2")


def notify_email_users(session, site_id, url, consecutive_fails):
    if consecutive_fails >= 2:
        site_watches = session.execute(
            select(SiteWatch).where(SiteWatch.site_id == site_id)
        ).scalars()

        for site_watch in site_watches:
            if not site_watch.notified_email and site_watch.notify_email:
                try:
                    user = session.execute(
                        select(User).where(User.id == site_watch.user_id)
                    ).scalar_one()
                except NoResultFound:
                    continue

                client.send_email(
                    Source="alerts@hrtbeat.io",
                    Destination={
                        "ToAddresses": [
                            user.email,
                        ]
                    },
                    Message={
                        "Subject": {"Data": "Outage", "Charset": "UTF-8"},
                        "Body": {
                            "Text": {
                                "Data": f"Your site {url} is currently experiencing an outage.",
                                "Charset": "UTF-8",
                            },
                        },
                    },
                )

                site_watch.notified_email = True
