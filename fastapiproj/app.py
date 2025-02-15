from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapiproj.config.database import get_session
from fastapiproj.models.model import User
from fastapiproj.schema.schema import (
    MessageUser,
    UserListDto,
    UserSchema,
    UserSchemaDto,
)

app = FastAPI()


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageUser,
    include_in_schema=False,
)
def new_route():
    return {'message': 'Feliz Natal!'}


@app.get('/users/get', response_model=UserListDto)
def read_all_users(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': user}


@app.get('/users/{user_id}', response_model=UserSchemaDto)
def get_user_per_id(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    return db_user


@app.post(
    '/users/add', status_code=HTTPStatus.CREATED, response_model=UserSchemaDto
)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username ja existe!',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Email ja existe!'
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserSchemaDto)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        db_user.username = user.username
        db_user.password = user.password
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username ou Email já existentes!',
        )


@app.delete('/users/{user_id}', response_model=MessageUser)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário deletado com sucesso!'}
