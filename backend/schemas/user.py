from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional

class User(BaseModel):
    username:str = Field(
        default=None,
        title="Please enter valid username",
        min_length=5,
    )
    email:EmailStr
    password:str

    @validator("username", "email", pre=True)
    def lowercase_strings(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value

class UserResponse(BaseModel):
    id: int
    username:str
    email:EmailStr

    class Config():
        orm_mode = True

class LoginResponse(BaseModel):
    username: str
    access_token: str
    token_type: str