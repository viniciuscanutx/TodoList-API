from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapiproj.config.database import get_session
from fastapiproj.config.security.security import (
    get_current_user,
)
from fastapiproj.models.model import User
from fastapiproj.schema.schema import UserListAdmDto

router = APIRouter(prefix='/adm', tags=['Adm - Routes'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/get', response_model=UserListAdmDto)
def read_all_users_adm(session: T_Session, current_user: T_CurrentUser):
    users = session.scalars(select(User)).all()

    return {'users': users}
