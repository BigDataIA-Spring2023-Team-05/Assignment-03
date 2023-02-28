from fastapi import APIRouter, status, HTTPException, Response, Depends
from utils import hashing, JWT_token
from schemas.user import User, UserResponse, LoginResponse
from sqlalchemy.orm import Session
from config import db
from repository import user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/user',
    tags=['User']
)

get_db = db.get_db


@router.post('/sign-up', status_code=status.HTTP_201_CREATED, response_model= UserResponse)
def sign_up_user(request: User, db: Session = Depends(get_db)):
    
    result = user.create(request = request, db = db)

    if result is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")
    else:
        return result



@router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = user.find_user(request.username, request.password, db = db)

    if result is HTTPException:
        return result
    
    return result