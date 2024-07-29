from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fast_zero.db.models import TodoState
from tests.conftest import TodoFactory


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


def test_list_todo_should_return_5_todos(
    session: Session, client: TestClient, user, token
):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todo_pagination_should_return_2_todos(
    session: Session, client: TestClient, user, token
):
    expected_todos = 2

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todo_filter_title_should_return_5_todos(
    session: Session, client: TestClient, user, token
):
    expected_todos = 5
    title = 'Test title filter'

    session.bulk_save_objects(
        TodoFactory.create_batch(5, title=title, user_id=user.id)
    )
    session.commit()

    response = client.get(
        f'/todos/?title={title}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todo_filter_description_should_return_5_todos(
    session: Session, client: TestClient, user, token
):
    expected_todos = 5
    description = 'Test description filter'

    session.bulk_save_objects(
        TodoFactory.create_batch(5, description=description, user_id=user.id)
    )
    session.commit()

    response = client.get(
        f'/todos/?description={description[:4]}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todo_filter_state_should_return_5_todos(
    session: Session, client: TestClient, user, token
):
    expected_todos = 5
    state = TodoState.done

    session.bulk_save_objects(
        TodoFactory.create_batch(5, state=state, user_id=user.id)
    )
    session.commit()

    response = client.get(
        f'/todos/?state={state.value}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_combined_should_return_5_todos(
    session: Session, client: TestClient, user, token
):
    expected_todos = 5
    title = 'Test todo combined'
    description = 'combined description'
    state = TodoState.done

    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title=title,
            description=description,
            state=state,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        f'/todos/?title={title}&description={description[:8]}&state={state.value}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_patch_todo(session: Session, client: TestClient, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'Test'


def test_patch_not_found_todo(client: TestClient, token):
    response = client.patch(
        '/todos/42',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_delete_todo(session: Session, client: TestClient, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


def test_delete_not_found_todo(client: TestClient, token):
    response = client.delete(
        '/todos/42',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
