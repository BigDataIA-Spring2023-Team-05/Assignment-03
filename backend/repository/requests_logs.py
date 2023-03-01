from sqlalchemy.orm import Session
from models.index import UserRequestsModel
from config import db
from fastapi import Depends, Request
from schemas.schemas import TokenData
from sqlalchemy.orm import Session
from utils.JWT_token import verify_token_v2

def create(request_endpoint: str, request_status: int,  db: Session, token:str):
    try:
        tokenData = verify_token_v2(token.split(" ")[1])
        if tokenData is None:
            return None
        
        new_request = UserRequestsModel(user_id= tokenData.id, endpoint = request_endpoint, statusCode = request_status)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return new_request
    except Exception as e:
        print(e)
        return None
    
# def update(request: UserRequestsModel, status_code: int, db: Session = Depends(db.get_db)):
#     try:
#         requestModel = db.query(UserRequestsModel).filter(UserRequestsModel.id == request.id)
        
#         requestModel.update({UserRequestsModel.status_code: status_code})
#         db.commit() 
#         return True
#     except Exception as e:
#         print(e)
#         return None