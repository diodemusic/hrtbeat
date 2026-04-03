# from sqlalchemy.orm import Session

# from ..core.engine import engine
# from ..core.tables import create_tables
# from ..models.sites import Site, Status
# from ..models.users import User

# create_tables()

# with Session(engine) as session:
#     user = User(
#         id=1,
#         username="Kieran",
#         email="example@example.com",
#         mobile_number="07112233445",
#     )
#     site = Site(url="example.com", status=Status.healthy)
#     session.add_all([user, site])
#     session.commit()
