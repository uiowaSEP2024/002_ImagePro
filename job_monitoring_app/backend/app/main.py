import os

from app.routers import (
    apikeys_router,
    auth_router,
    events_router,
    users_router,
    study_configurations_router,
    reporting_router,
    studies_router,
)
from config import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

allow_origins = os.environ.get("ALLOW_ORIGINS", "http://localhost:3000").split(",")
allow_origins.append("http://0.0.0.0:8000")
allow_origins.append("http://localhost:8000")
allow_origins.append("http://frontend:3000")
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
app.include_router(events_router)
app.include_router(study_configurations_router)
app.include_router(reporting_router)
app.include_router(studies_router)

# Create handler for AWS lambda
handler = Mangum(app, lifespan="on")
