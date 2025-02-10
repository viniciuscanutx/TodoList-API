from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fastapiproj.schema.schema import (
    MessageUser,
    UserDB,
    UserListDto,
    UserSchema,
    UserSchemaDto,
)

app = FastAPI()

database = []


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageUser,
    include_in_schema=False,
)
def new_route():
    return {'message': 'Feliz Natal!'}


@app.get('/users/get', response_model=UserListDto)
def read_all_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserSchemaDto)
def get_user_per_id(user_id: int):
    user_with_id = database[user_id - 1]

    return user_with_id


@app.post(
    '/users/add', status_code=HTTPStatus.CREATED, response_model=UserSchemaDto
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.put('/users/{user_id}', response_model=UserSchemaDto)
def update_user(user_id: int, user: UserSchema):
    # verificação para ver se o usuário realmente existe na db
    if user_id > len(database) or user_id < 1:
        # Exception caso não exista o usuario.
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    # Dumpando o ID do usuario através da USERDB.
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    # Substituindo a posição do ID informado na url.
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=MessageUser)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        # Exception caso não exista o usuario.
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    del database[user_id - 1]

    return {'message': 'Usuário deletado com sucesso!'}
