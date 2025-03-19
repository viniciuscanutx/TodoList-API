from fastapi import APIRouter

from fastapiproj.schema.todo_schema import TodoPublic, TodoSchema

router = APIRouter(prefix='/todos', tags=['Todos'])


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema): ...
