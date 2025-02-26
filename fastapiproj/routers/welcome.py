from http import HTTPStatus

from fastapi import APIRouter

from fastapiproj.routers import auth, users
from fastapiproj.schema.schema import (
    MessageUser,
)

router = APIRouter(tags=['Welcome'], include_in_schema=False)


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageUser,
    include_in_schema=False,
)
def new_route():
    return {'message': 'Working!'}
