from fastapi import status
from fastapi.testclient import TestClient


def test_read_root_should_return_ok_and_hello_world(client: TestClient):
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Hello, World!'}
