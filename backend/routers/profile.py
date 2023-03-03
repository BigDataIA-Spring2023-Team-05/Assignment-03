from fastapi import APIRouter, status, HTTPException, Response, Depends
from config import db
from schemas.index import UserDashboardResponse
from schemas.schemas import TokenData
from middleware.oauth2 import get_current_user
from sqlalchemy.orm import Session
from repository.service_plans import get_plan_by_user_id
from repository.requests_logs import get_user_api_request_in_hr
from repository.user import find_user_api_key

router = APIRouter(
    prefix='/profile',
    tags=['Profile']
)

get_db = db.get_db


@router.get('/api-hits', response_model=UserDashboardResponse)
def get_user_api_hits(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    api_key = find_user_api_key(get_current_user.id, db)
    plan = get_plan_by_user_id(get_current_user.id, db)
    total_api_hits, total_successful_api = get_user_api_request_in_hr(get_current_user.id, db= db)

    failed_api_hits = total_api_hits - total_successful_api

    return UserDashboardResponse(
        plan= plan,
        total_api_hits_in_hr= total_api_hits,
        total_successful_api_hits_in_hr = total_successful_api,
        total_failed_api_hits_in_hr = failed_api_hits,
        api_key= api_key
    )
