from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import env

engine = create_engine(env.DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
