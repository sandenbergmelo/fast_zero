from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from fast_zero.custom_types.annotated_types import (
    T_CurrentUser,
    T_OAuthForm,
    T_Session,
)
from fast_zero.db.models import User
from fast_zero.schemas import Token
from fast_zero.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
def login_for_access_token(session: T_Session, form_data: T_OAuthForm):
    form_username, form_password = (
        form_data.username.lower(),
        form_data.password,
    )

    user = session.scalar(select(User).where(User.email == form_username))

    if not user or not verify_password(form_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token({'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: T_CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'Bearer'}
