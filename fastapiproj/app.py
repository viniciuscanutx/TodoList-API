from http import HTTPStatus

from fastapi import FastAPI

from fastapiproj.schema.schema import Message, UserDB, UserSchema
from fastapiproj.schema.schemaDto import UserListDto, UserSchemaDto

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def new_route():
    return {'message': 'Feliz Natal!', 'value': 11.99, 'author': 'João'}


@app.get('/users/get', response_model=UserListDto)
def read_all_users():
    return {'users': database}


@app.post(
    '/users/add', status_code=HTTPStatus.CREATED, response_model=UserSchemaDto
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id
