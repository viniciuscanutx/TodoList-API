from http import HTTPStatus

from fastapi import FastAPI

from fastapiproj.routers import auth, users
from fastapiproj.schema.schema import (
    MessageUser,
)

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageUser,
    include_in_schema=False,
)
def new_route():
    return {'message': 'Working!'}
