from sqlalchemy.orm import Session
from models.index import UserModel, ServicePlanModel
from schemas.index import User, LoginResponse, UserPlan, Plan
from utils import hashing, JWT_token
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

def create(request: User, db: Session):
    try:
        new_user = UserModel(username=request.username, email=request.email, password= hashing.Hash().get_hashed_password(request.password), planId = request.planId, apiKey = str(uuid.uuid4()))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print(e)
        return None
    
def find_user(username: str, password: str, db: Session):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with the username '{username}' not found"
            )
    
    if not hashing.Hash().verify_password(user.password, password=password):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="invalid credentials"
            )
    
    access_token = JWT_token.create_access_token(data={"id": user.id, "username": user.username, "account_type": ""})
    
    return LoginResponse(username= str(user.username), access_token= access_token, token_type= 'bearer')

def find_user_by_email(email:str, db: Session):
    user = db.query(UserModel).filter(UserModel.email == email).first()


    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with the email '{email}' not found"
            )
    
    return user


def change_user_password_to_new(email: str, new_pasword:str, db:Session):
    user:UserModel = db.query(UserModel).filter(UserModel.email == email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} not found")
    
    user.password = hashing.Hash().get_hashed_password(new_pasword)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
