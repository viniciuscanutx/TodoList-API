from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapiproj.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app) #Arrange

    response = client.get('/') #Act

    assert response.status_code == HTTPStatus.OK #Assert 
    assert response.json() == { #Assert 
        'message': 'Feliz Natal!',
        'anothermessage': 'Brutalist!',
    }
