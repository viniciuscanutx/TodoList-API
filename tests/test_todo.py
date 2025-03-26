from http import HTTPStatus

from fastapiproj.models.model import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos/create',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'category': 'Test',
            'state': 'draft',
        },
    )
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'category': 'Test',
        'state': 'draft',
    }


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))

    session.commit()

    response = client.get(
        '/todos/get',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test Todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/get?title=Test Todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_category_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, category='Work')
    )
    session.commit()

    response = client.get(
        '/todos/get?category=Work',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_state_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.done)
    )
    session.commit()

    response = client.get(
        '/todos/get?state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))

    session.commit()

    response = client.get(
        '/todos/get?offset=2&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_empty(client, token):
    response = client.get(
        '/todos/get',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'todos': []}


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/delete/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task deletada com sucesso!'}


def test_delete_todo_not_found(session, client, user, token):
    response = client.delete(
        f'/todos/delete/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Todo não encontrado!'}


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/patch/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Todo não encontrado!'}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/patch/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'
