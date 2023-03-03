from fastapi import FastAPI

from app.models.base import ensure_tables_created
from app.routers import users_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


app.include_router(users_router)
