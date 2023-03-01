from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from config import db
from repository import service_plans as servicePlan
from schemas.index import Plan
from typing import List



router = APIRouter(
    prefix='/service-plan',
    tags=['Service Plan']
)


@router.get('/options', status_code=status.HTTP_200_OK, response_model= List[Plan])
def sign_up_user(db: Session = Depends(db.get_db)):
    result = servicePlan.get_plans(db = db)

    return result

