from pydantic import BaseModel, EmailStr


class MessageUser(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int
