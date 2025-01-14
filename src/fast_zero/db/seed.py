from pathlib import Path

import alembic
import alembic.command
import factory
import factory.fuzzy
from alembic.config import Config
from rich import print
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from fast_zero.db.models import Todo, TodoState, User
from fast_zero.helpers.security import get_password_hash
from fast_zero.helpers.settings import env


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(
        lambda obj: get_password_hash(f'{obj.username}+password')
    )


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text', max_nb_chars=50)
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = factory.fuzzy.FuzzyInteger(1, 5)


alembic_config = Config(
    Path(__file__).parent.parent.parent.parent / 'alembic.ini'
)

engine = create_engine(env.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Delete all tables
print('[bold yellow]Dropping database...[/]')
alembic.command.downgrade(alembic_config, 'base')
session.execute(text('DROP TYPE IF EXISTS todostate'))
session.commit()
print('[bold green]Database dropped![/]')

# Create all tables
print('[bold yellow]Creating database...[/]')
alembic.command.upgrade(alembic_config, 'head')
print('[bold green]Database created![/]')

users = UserFactory.create_batch(5)
todos = TodoFactory.create_batch(10)

users.insert(
    0,
    User(
        username='admin',
        password=get_password_hash('admin'),
        email='admin@admin.com',
    ),
)

print('[bold yellow]Seeding database...[/]')
session.add_all(users)
session.commit()
session.add_all(todos)
session.commit()
print('[bold green]Database seeded![/]')
