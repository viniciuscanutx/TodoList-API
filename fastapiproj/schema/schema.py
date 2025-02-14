from pydantic import BaseModel, ConfigDict, EmailStr


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
