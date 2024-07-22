from http import HTTPStatus


def test_read_root_should_return_ok_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'John Doe',
            'email': 'john@doe.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'John Doe',
        'email': 'john@doe.com',
    }


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'John Doe', 'email': 'john@doe.com'}]
    }


def test_get_user_by_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'John Doe',
        'email': 'john@doe.com',
    }


def test_delete_not_found_user_by_id(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_users(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Hello',
            'email': 'hello@world.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Hello',
        'email': 'hello@world.com',
    }


def test_update_not_found_user(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'Hello',
            'email': 'hello@world.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_users(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_found_user(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
