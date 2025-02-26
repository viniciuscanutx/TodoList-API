from http import HTTPStatus

from fastapi import FastAPI

from fastapiproj.routers import auth, users, welcome
from fastapiproj.schema.schema import (
    MessageUser,
)

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(welcome.router)
