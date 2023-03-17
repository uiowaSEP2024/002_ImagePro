from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.routers import users_router, auth_router, apikeys_router

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


app.include_router(users_router)
app.include_router(apikeys_router)
app.include_router(auth_router)

# Create handler for AWS lambda
handler = Mangum(app, lifespan="off")
