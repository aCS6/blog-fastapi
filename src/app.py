from fastapi import (
    FastAPI, 
    HTTPException , 
    status , 
    Response,
    Depends
)
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import get_db 
from .utils import hash
from .routers import post , user , auth , like

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["https://www.google.com"] # allowed domains
origins =["*"]  # for make a public api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index( db: Session = Depends(get_db) ):
    return {"message" : "hello world"}

app.include_router(
    auth.router,
    prefix = "/login",
    tags = ["Authentication"]
)

app.include_router(
    post.router,
    prefix = "/posts",
    tags = ["Post"]
)

app.include_router(
    user.router,
    prefix = "/users",
    tags = ["User"]
)

app.include_router(
    like.router,
    prefix="/like",
    tags=['like']
)
