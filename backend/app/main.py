from fastapi import FastAPI

from app.config.database import ensure_tables_created
from app.routers import users_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


ensure_tables_created()

app.include_router(users_router)
