from http import HTTPStatus
from fastapi import FastAPI
from fastapiproj.schema.schema import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def new_route():
    return {'message': 'Feliz Natal!', 'value': 11, 'author': 'João'}
