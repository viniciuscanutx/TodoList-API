from http import HTTPStatus

from fastapiproj.schema.schema import UserSchemaDto


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {  # Assert
        'message': 'Working!'
    }


def test_create_user(client):
    response = client.post(
        '/users/add',
        json={
            'username': 'testusername',
            'email': 'teste@testegenio.com',
            'password': '1235',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'teste@testegenio.com',
    }


def test_read_users(client):
    response = client.get('/users/get')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserSchemaDto.model_validate(user).model_dump()

    response = client.get('/users/get')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_create_user_should_return_400_username_exists(client, user):
    response = client.post(
        '/users/add',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username ja existe!'}


def test_create_user_should_return_400_email_exists__exercicio(client, user):
    response = client.post(
        '/users/add',
        json={
            'username': 'alice',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ja existe!'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário deletado com sucesso!'}


def test_update_user_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'testusername2',
            'email': 'teste@testegenio.com',
            'password': '12353',
            'id': 999,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_delete_user_not_found(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'Usuário não encontrado!'}
