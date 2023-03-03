from sqlalchemy.orm import Session
from models.index import UserModel, ServicePlanModel, Role
from schemas.index import User, LoginResponse, UserPlan, Plan
from utils import hashing, JWT_token
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

from awscloud.cloudwatch.logger import write_user_login_logs, write_user_sign_up_logs

def create(request: User, db: Session):
    try:
        new_user = UserModel(username=request.username, email=request.email, password= hashing.Hash().get_hashed_password(request.password), planId = request.planId, apiKey = str(uuid.uuid4()))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        write_user_sign_up_logs(f"User created a new account: \nusername: {request.username}\nemail: {request.email}, planId: {request.planId}")
        return new_user
    except Exception as e:
        print(e)
        return None
    
def find_user(username: str, password: str, db: Session):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user:
        write_user_login_logs(f"{username} not present in Database!")
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with the username '{username}' not found"
            )
    
    if not hashing.Hash().verify_password(user.password, password=password):
        write_user_login_logs(f"{username} tried to authenticate with invalid credentials")

        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="invalid credentials"
            )
    
    access_token = JWT_token.create_access_token(data={"id": user.id, "username": user.username, "account_type": 1 if user.userType == Role.Admin else 2})
    write_user_login_logs(f"{username} successfully logged in!")
    

    return LoginResponse(username= str(user.username), access_token= access_token, token_type= 'bearer', userType=user.userType)

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

def find_user_api_key(user_id:int, db: Session) -> str:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User not found"
            )
    
    return str(user.apiKey)
