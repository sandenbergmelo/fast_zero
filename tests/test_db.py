from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.db.models import User


def test_create_user(session: Session):
    user = User(username='Hello', email='hello@world.com', password='secret')

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'hello@world.com')
    )

    assert user.username == result.username
