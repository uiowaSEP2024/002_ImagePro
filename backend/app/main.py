import os

from app.routers import (
    apikeys_router,
    auth_router,
    jobs_router,
    users_router,
    events_router,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from config import config

app = FastAPI()

allow_origins = os.environ.get("ALLOW_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.on_event("startup")
async def startup_event():
    config.setup()
    print("Running with allowed origins:", allow_origins)


app.include_router(users_router)
app.include_router(apikeys_router)
app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(events_router)

# Create handler for AWS lambda
handler = Mangum(app, lifespan="off")
