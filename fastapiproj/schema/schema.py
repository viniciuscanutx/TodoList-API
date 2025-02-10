from pydantic import BaseModel, EmailStr


class MessageUser(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserSchemaDto(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserListDto(BaseModel):
    users: list[UserSchemaDto]
