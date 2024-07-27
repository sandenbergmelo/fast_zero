from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from fast_zero.custom_types.annotated_types import T_CurrentUser, T_Session
from fast_zero.db.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()

    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(session: T_Session, limit: int = 10, offset: int = 0):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@router.get('/{id}', response_model=UserPublic)
def get_user_by_id(id: int, session: T_Session):
    user = session.get(User, id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    return user


@router.put('/{id}', response_model=UserPublic)
def update_user(
    id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permission',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{id}', response_model=Message)
def delete_user(
    id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permission',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
