from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from . service_plan import Plan
from models.user import Role
class User(BaseModel):
    username:str = Field(
        default=None,
        title="Please enter valid username",
        min_length=5,
    )
    email:EmailStr
    password:str = Field(
        min_length=8
    )
    planId: int = Field(
        default=1,
        title="Please enter the plan ID (Free - 1, Gold - 2, Platinum - 3)"
        )

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

class UserPlan(BaseModel):
    id: int
    username:str
    email:EmailStr
    plan: Plan
    class Config():
        orm_mode = True

class LoginResponse(BaseModel):
    username: str
    userType: Role
    access_token: str
    token_type: str

class ForgotPassword(BaseModel):
    email:EmailStr

class VerifyForgotPassword(BaseModel):
    email:EmailStr
    otp:int

class PasswordResetRequest(BaseModel):
    email:EmailStr
    otp:int
    new_password:str = Field(
        min_length=8
    )
    confirm_password:str = Field(
        min_length=8
    )