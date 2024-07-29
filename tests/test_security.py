import jwt
from fastapi import status
from fastapi.testclient import TestClient

from fast_zero.helpers.security import create_access_token
from fast_zero.helpers.settings import env


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)
    decoded = jwt.decode(token, env.SECRET_KEY, [env.ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']


def test_invalid_token(client: TestClient):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_without_sub(client: TestClient):
    token = create_access_token({'sub': ''})

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not_found(client: TestClient):
    token = create_access_token({'sub': 'no_user@no_user.com'})

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
