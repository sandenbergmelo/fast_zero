from fastapi import status
from fastapi.testclient import TestClient
from freezegun import freeze_time


def test_get_token(client: TestClient, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']


def test_token_expired_after_time(client: TestClient, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == status.HTTP_200_OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'test',
                'email': 'test@test.test',
                'password': 'test',
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token has expired'}


def test_token_wrong_email(client: TestClient, user):
    response = client.post(
        '/auth/token',
        data={'username': 'incorrect', 'password': user.clean_password},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(client: TestClient, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'incorrect'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client: TestClient, token):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['access_token']
    assert data['token_type'] == 'Bearer'


def test_token_expired_do_not_refresh(client: TestClient, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == status.HTTP_200_OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token has expired'}
