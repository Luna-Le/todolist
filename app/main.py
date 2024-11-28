from fastapi import FastAPI
from .routers import auth, user, task
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine



app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #which domains are allowed to talk to our api
    allow_credentials=True,
    allow_methods=["*"], #which methods are allowed
    allow_headers=["*"], ##which headers are allowed
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

