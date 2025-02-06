from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapiproj.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {  # Assert
        'message': 'Feliz Natal!',
        'value': 11.99,
        'author': 'João',
    }


def test_create_user():
    client = TestClient(app)

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
