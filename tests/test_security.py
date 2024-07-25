from http import HTTPStatus

import jwt
from fastapi.testclient import TestClient

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, [ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']


def test_get_token(client: TestClient, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']


def test_invalid_token(client: TestClient):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
