from fastapi import FastAPI

from fastapiproj.routers import adm_routes, auth, users, welcome

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(welcome.router)
app.include_router(adm_routes.router)
