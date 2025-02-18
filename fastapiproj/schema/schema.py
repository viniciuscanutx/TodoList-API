from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class MessageUser(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaToken(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime


class UserSchemaDto(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserListDto(BaseModel):
    users: list[UserSchemaDto]


class UserListAdmDto(BaseModel):
    users: list[UserSchemaToken]


class Token(BaseModel):
    access_token: str
    token_type: str
