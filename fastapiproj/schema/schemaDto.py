from pydantic import BaseModel, EmailStr


class UserSchemaDto(BaseModel):
    id: int
    username: str
    email: EmailStr
