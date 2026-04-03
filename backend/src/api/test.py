from sqlalchemy.orm import Session

from ..core.engine import engine
from ..core.tables import create_tables
from ..models.users import User

create_tables()

with Session(engine) as session:
    user = User(
        id=1,
        username="Kieran",
        email="example@example.com",
        mobile_number="07112233445",
    )
    session.add(user)
    session.commit()
