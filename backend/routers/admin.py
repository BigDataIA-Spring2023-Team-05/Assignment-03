from fastapi import APIRouter, status, HTTPException, Response, Depends
from config import db
from schemas.index import UserDashboardResponse
from schemas.schemas import TokenData
from middleware.oauth2 import get_current_user
from sqlalchemy.orm import Session
from repository.requests_logs import get_user_api_request_data_by_hour_for_specific_date, get_all_users_for_admin
from repository.user import find_user_api_key
from fastapi.responses import JSONResponse
from datetime import datetime


router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

get_db = db.get_db

@router.get('/all-users')
def get_all_users(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    users = get_all_users_for_admin(db= db)

    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'success': True, 
                    "users": users,
                }
            )



@router.get('/api-hits-count')
def get_user_api_hits_for_particular_days(id: int, date_request: str, get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    requested_date = datetime.strptime(date_request, "%m/%d/%Y").date()
    print(requested_date)
    total_api_hits = get_user_api_request_data_by_hour_for_specific_date(requested_date, id, db= db)


    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'success': True, 
                    "api_req": total_api_hits,
                }
            )

