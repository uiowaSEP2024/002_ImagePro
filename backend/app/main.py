from fastapi import Depends, FastAPI

from app.routers import users

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


app.include_router(users.router)
