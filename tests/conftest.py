import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.db.connection import get_session
from fast_zero.db.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture
def client(session: Session):
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = lambda: session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session: Session):
    clean_password = 'test_pass'

    user = User(
        username='Test',
        email='test@test.com',
        password=get_password_hash(clean_password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = clean_password  # Monkey Patch

    return user


@pytest.fixture
def token(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
