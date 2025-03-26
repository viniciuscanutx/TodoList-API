from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapiproj.config.database import get_session
from fastapiproj.config.security.security import get_current_user
from fastapiproj.models.model import Todo, TodoState, User
from fastapiproj.schema.schema import MessageUser
from fastapiproj.schema.todo_schema import (
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)

router = APIRouter(prefix='/todos', tags=['Todos'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/create', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,  # type: ignore
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        category=todo.category,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/get', response_model=TodoList)
def list_todos(  # noqa
    session: Session,  # type: ignore
    user: CurrentUser,
    title: str | None = None,
    category: str | None = None,
    state: TodoState | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.where(Todo.title.contains(title))

    if category:
        query = query.where(func.lower(Todo.category) == func.lower(category))

    if state:
        query = query.where(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.patch('/patch/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int,
    session: Session,  # type: ignore
    user: CurrentUser,
    todo: TodoUpdate,
):
    db_todo = session.scalar(
        select(Todo).where(
            Todo.user_id == user.id,
            Todo.id == todo_id,
        )
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Todo não encontrado!'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/delete/{todo_id}', response_model=MessageUser)
def delete_todo(
    todo_id: int,
    session: Session,  # type: ignore
    user: CurrentUser,
):
    todo = session.scalar(
        select(Todo).where(
            Todo.user_id == user.id,
            Todo.id == todo_id,
        )
    )

    if not todo:
        raise HTTPException(status_code=404, detail='Todo não encontrado!')

    session.delete(todo)
    session.commit()

    return {'message': 'Task deletada com sucesso!'}
