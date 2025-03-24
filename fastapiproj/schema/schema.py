from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class MessageUser(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaDto(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserListDto(BaseModel):
    users: list[UserSchemaDto]


class UserSchemaToken(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime


class UserListAdmDto(BaseModel):
    users: list[UserSchemaToken]


class UserCreateDto(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserListCreate(BaseModel):
    users: list[UserCreateDto]


class Token(BaseModel):
    access_token: str
    token_type: str
