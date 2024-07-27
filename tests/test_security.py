import jwt
from fastapi import status
from fastapi.testclient import TestClient

from fast_zero.security import create_access_token
from fast_zero.settings import env


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
