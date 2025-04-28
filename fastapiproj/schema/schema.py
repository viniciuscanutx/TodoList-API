from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class MessageUser(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaDto(BaseModel):
    id: int
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
    model_config = ConfigDict(from_attributes=True)


class UserListCreate(BaseModel):
    users: list[UserCreateDto]


class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
