from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapiproj.config.database import get_session
from fastapiproj.config.security.security import (
    get_current_user,
    get_password_hash,
)
from fastapiproj.models.model import User
from fastapiproj.schema.schema import (
    MessageUser,
    UserCreateDto,
    UserListDto,
    UserSchema,
    UserSchemaDto,
    UserUpdateSchema,
)

router = APIRouter(prefix='/users', tags=['Users'])

# Vars
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/get', response_model=UserListDto)
def read_all_users(session: T_Session, skip: int = 0, limit: int = 10):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': user}


@router.get('/me', response_model=UserSchemaDto)
def get_current_user_info(current_user: T_CurrentUser):
    return current_user


@router.get('/{user_id}', response_model=UserSchemaDto)
def get_user_per_id(user_id: int, session: T_Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!'
        )

    return db_user


@router.post(
    '/add', status_code=HTTPStatus.CREATED, response_model=UserCreateDto
)
def create_user(user: UserSchema, session: T_Session):
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


@router.put('/{user_id}', response_model=UserSchemaDto)
def update_user(
    user_id: int,
    user: UserUpdateSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Você não tem permissão!',
        )

    
    if user.username is not None:
        if user.username != current_user.username:
            existing_username = (
                session.query(User)
                .filter(User.username == user.username)
                .filter(User.id != user_id)
                .first()
            )
            if existing_username:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT, detail='Username já existente!'
                )
            current_user.username = user.username

    
    if user.email is not None:
        if user.email != current_user.email:
            existing_email = (
                session.query(User)
                .filter(User.email == user.email)
                .filter(User.id != user_id)
                .first()
            )
            if existing_email:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT, detail='Email já existente!'
                )
            current_user.email = user.email

    
    if user.password is not None:
        current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=MessageUser)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Você não tem permissão!',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário deletado com sucesso!'}
