from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str
    value: float
    author: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int
