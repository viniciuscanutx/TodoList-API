from typing import Optional

from pydantic import BaseModel

from fastapiproj.models.model import TodoState


class TodoSchema(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    state: TodoState


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]
