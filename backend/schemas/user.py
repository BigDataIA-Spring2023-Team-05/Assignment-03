from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username:str
    email:str
    password:str

class UserResponse(BaseModel):
    id: int
    username:str
    email:str

    class Config():
        orm_mode = True

class LoginResponse(BaseModel):
    username: str
    access_token: str
    token_type: str