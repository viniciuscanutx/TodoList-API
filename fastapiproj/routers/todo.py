from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapiproj.config.database import get_session
from fastapiproj.config.security.security import get_current_user
from fastapiproj.models.model import Todo, User
from fastapiproj.schema.todo_schema import TodoPublic, TodoSchema

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

    return todo
