from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import ensure_tables_created
from app.routers import users_router

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


# TODO: take this out once we have migrations
ensure_tables_created()

app.include_router(users_router)
