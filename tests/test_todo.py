from fastapi import status
from fastapi.testclient import TestClient


def test_create_todo(client: TestClient, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'title': 'Test',
        'description': 'Test todo description',
        'state': 'draft',
    }
