from sqlalchemy.orm import Session
from models.index import UserRequestsModel
from config import db
from fastapi import Depends, Request
from schemas.schemas import TokenData
from utils.JWT_token import verify_token_v2
from models.index import UserModel, ServicePlanModel, UserRequestsModel
from utils.redis import islimiter
from config import db
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

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
    

def get_user_specific_api_rate_limit(request:Request, db: Session = Depends(db.get_db)):

    try:
        if request.headers.get('Authorization') is not None:
            tokenData = verify_token_v2(request.headers['Authorization'].split(" ")[1])
            print(tokenData)
            if tokenData is None:
                return None
            
            print(tokenData)
        
        user: UserModel = db.query(UserModel).filter(UserModel.id == tokenData.id).join(ServicePlanModel).first()
        return islimiter(user.id, user.plan.requestLimit)
    
    except Exception as e:
        print(e)


def get_user_api_request_in_hr(user_id:int, db: Session):
    one_hour_interval_before = datetime.now() - timedelta(hours=1)

    total_api_hits = db.query(UserRequestsModel).filter(and_(UserRequestsModel.created_date >= one_hour_interval_before, UserRequestsModel.user_id == user_id)).count()
    total_succesfull_api_hits = db.query(UserRequestsModel).filter(
        and_(
            UserRequestsModel.created_date >= one_hour_interval_before, 
            UserRequestsModel.user_id == user_id, 
            or_(
                UserRequestsModel.statusCode == 200, 
                UserRequestsModel.statusCode == 201
                )
            )).count()

    return total_api_hits, total_succesfull_api_hits
