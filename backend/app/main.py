from fastapi import FastAPI

from app.models.base import ensure_tables_created
from app.routers import users_router, apikeys_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


# TODO: take this out once we have migrations
ensure_tables_created()

app.include_router(users_router)
app.include_router(apikeys_router)
