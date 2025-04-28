from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapiproj.routers import adm_routes, auth, todo, users, welcome

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(welcome.router)
app.include_router(adm_routes.router)
app.include_router(todo.router)
