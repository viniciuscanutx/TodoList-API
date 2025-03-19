from models.model import TodoState
from pydantic import BaseModel


class TodoSchema(BaseModel):
    title: str
    description: str
    category: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
