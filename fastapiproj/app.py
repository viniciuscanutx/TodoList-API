from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapiproj.config.database import get_session
from fastapiproj.config.security.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from fastapiproj.models.model import User
from fastapiproj.schema.schema import (
    MessageUser,
    Token,
    UserListAdmDto,
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
    return {'message': 'Working!'}


@app.get('/users/get', response_model=UserListDto)
def read_all_users(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': user}


@app.get('/users/nuget', response_model=UserListAdmDto)
def read_all_users_adm(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    user = session.scalars(select(User)).all()
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
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserSchemaDto)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Você não tem permissão!')

    existing_username = (
        session.query(User).filter(User.username == user.username).first()
    )
    existing_email = (
        session.query(User).filter(User.email == user.email).first()
    )

    if existing_username:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Username já existente!'
        )

    if existing_email:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email já existente!'
        )

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', response_model=MessageUser)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Você não tem permissão!',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário deletado com sucesso!'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou Senha Incorretos!',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou Senha Incorretos!',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
