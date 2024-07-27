from fastapi import status
from fastapi.testclient import TestClient

from fast_zero.schemas import UserPublic


def test_create_user(client: TestClient):
    response = client.post(
        '/users',
        json={
            'username': 'John Doe',
            'email': 'john@doe.com',
            'password': 'secret',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': 1,
        'username': 'John Doe',
        'email': 'john@doe.com',
    }


def test_create_user_username_already_exists(client: TestClient, user):
    response = client.post(
        '/users',
        json={
            'username': 'Test',
            'email': 'different@email.com',
            'password': 'does not matter',
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exists(client: TestClient, user):
    response = client.post(
        '/users',
        json={
            'username': 'Different Username',
            'email': 'test@test.com',
            'password': 'does not matter',
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users_empty(client: TestClient):
    response = client.get('/users')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client: TestClient, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'users': [user_schema]}


def test_get_user_by_id(client: TestClient, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_schema


def test_get_not_found_user_by_id(client: TestClient):
    response = client.get('/users/2')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_users(client: TestClient, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Hello',
            'email': 'hello@world.com',
            'password': '123',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'username': 'Hello',
        'email': 'hello@world.com',
    }


def test_update_not_found_user(client: TestClient, user, token):
    # Delete the user before the test
    client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Hello',
            'email': 'hello@world.com',
            'password': '123',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_users(client: TestClient, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_found_user(client: TestClient, user, token):
    # Delete the user before the test
    client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}