from fastapi import APIRouter, status, HTTPException, Response, Depends
from config import db
from schemas.index import UserDashboardResponse
from schemas.schemas import TokenData
from middleware.oauth2 import get_current_user
from sqlalchemy.orm import Session
from repository.service_plans import get_plan_by_user_id
from repository.requests_logs import get_user_api_request_in_hr, get_user_api_request_in_day, get_user_api_request_data_by_hour_for_specific_date, get_all_apis_list_with_count
from repository.user import find_user_api_key
from fastapi.responses import JSONResponse
from datetime import datetime

router = APIRouter(
    prefix='/profile',
    tags=['Profile']
)

get_db = db.get_db


@router.get('/api-hits-count', response_model=UserDashboardResponse)
def get_user_api_hits(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    api_key = find_user_api_key(get_current_user.id, db)
    plan = get_plan_by_user_id(get_current_user.id, db)
    total_api_hits, total_successful_api = get_user_api_request_in_hr(get_current_user.id, db= db)

    failed_api_hits = total_api_hits - total_successful_api

    return UserDashboardResponse(
        plan= plan,
        username = str(get_current_user.username),
        total_api_hits_in_hr= total_api_hits,
        total_successful_api_hits_in_hr = total_successful_api,
        total_failed_api_hits_in_hr = failed_api_hits,
        api_key= api_key
    )

@router.get('/api-hits-previous-days')
def get_user_api_hits_count_for_previus_days(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    total_api_hits, total_successful_api = get_user_api_request_in_day(get_current_user.id, db= db)

    failed_api_hits = total_api_hits - total_successful_api

    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'success': True, 
                    "total_api_hits_in_previous_day": total_api_hits,
                    "total_successful_api_hits_in_previous_day": total_successful_api,
                    "total_failed_api_hits_in_previous_day": failed_api_hits
                }
            )



@router.get('/api-hits')
def get_user_api_hits_for_particular_days(date_request: str, get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    requested_date = datetime.strptime(date_request, "%m/%d/%Y").date()
    print(requested_date)

    total_api_hits = get_user_api_request_data_by_hour_for_specific_date(requested_date, get_current_user.id, db= db)


    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'success': True, 
                    "total_api_hits_in_previous_day": total_api_hits,
                }
            )




@router.get('/admin/all-apis-hits-with-count')
def get_all_apis_list(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):
    return get_all_apis_list_with_count(db)