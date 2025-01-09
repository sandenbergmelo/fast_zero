from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.db.connection import get_session
from fast_zero.db.models import User
from fast_zero.helpers.settings import env


class CredentialsException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = 'Could not validate credentials',
        headers: dict[str, str] | None = {'WWW-Authenticate': 'Bearer'},
    ) -> None:
        super().__init__(status_code, detail, headers)


pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    data_to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    data_to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(data_to_encode, env.SECRET_KEY, env.ALGORITHM)

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, env.SECRET_KEY, [env.ALGORITHM])
        username: str = payload['sub']

        if not username:
            raise CredentialsException()

    except ExpiredSignatureError:
        raise CredentialsException(detail='Token has expired')

    except PyJWTError:
        raise CredentialsException()

    user = session.scalar(select(User).where(User.email == username))

    if not user:
        raise CredentialsException()

    return user
