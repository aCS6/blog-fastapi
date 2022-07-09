from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr 
    password: str


class UserView(BaseModel):
    id: int
    email: EmailStr 

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostView(Post):
    id: int
    author: UserView
    total_like: int = None
    
    class Config:
        orm_mode = True 



class Like(BaseModel):
    post_id: int 