from fastapi import APIRouter, status, HTTPException, Response, Depends
from config import db
from schemas.index import UserDashboardResponse
from schemas.schemas import TokenData
from middleware.oauth2 import get_current_user
from sqlalchemy.orm import Session
from repository.requests_logs import get_user_api_request_data_by_hour_for_specific_date, get_all_users_for_admin, get_all_apis_list_with_count
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



@router.get('/api-hits-count/user/{user_id}')
def get_user_api_hits_for_particular_days_for_user(user_id, date_request: str, get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    requested_date = datetime.strptime(date_request, "%m/%d/%Y").date()
    print(requested_date)
    total_api_hits = get_user_api_request_data_by_hour_for_specific_date(requested_date, user_id, db= db)
    
    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'success': True, 
                    "api_req": total_api_hits,
                }
            )


@router.get('/all-apis-hits-with-count')
def get_all_apis_list(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):
    return get_all_apis_list_with_count(db)