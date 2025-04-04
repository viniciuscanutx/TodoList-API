from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from fastapiproj.models.model import TodoState


class TodoBase(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    state: TodoState
    updated_at: datetime
    created_at: datetime


class TodoSchema(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    state: TodoState


class TodoPublic(TodoBase):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    state: TodoState | None = None
