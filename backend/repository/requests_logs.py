from typing import List
from sqlalchemy.orm import Session
from models.index import UserRequestsModel
from config import db
from fastapi import Depends, Request
from schemas.schemas import TokenData, UserRequests
from utils.JWT_token import verify_token_v2
from models.index import UserModel, ServicePlanModel, UserRequestsModel
from utils.redis import islimiter
from config import db
from datetime import datetime, timedelta, date
from sqlalchemy import and_, or_, Date, cast, distinct, tuple_
from sqlalchemy.sql import func


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
    one_hour_interval_before = datetime.utcnow() - timedelta(hours=1)

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


def get_user_api_request_in_day(user_id:int, db: Session):
    previous_day = date.today() - timedelta(days= 1)

    total_api_hits = db.query(UserRequestsModel).filter(and_(cast(UserRequestsModel.created_date, Date) == previous_day, UserRequestsModel.user_id == user_id)).count()
    total_succesfull_api_hits = db.query(UserRequestsModel).filter(
        and_(
            cast(UserRequestsModel.created_date, Date) == previous_day,
            UserRequestsModel.user_id == user_id, 
            or_(
                UserRequestsModel.statusCode == 200, 
                UserRequestsModel.statusCode == 201
                )
            )).count()

    return total_api_hits, total_succesfull_api_hits

def get_user_api_request_data_by_hour_for_specific_date(date_requested: Date, user_id:int, db: Session):
    record = [z.to_json() for z in db.query(UserRequestsModel).filter(and_(cast(UserRequestsModel.created_date, Date) >= date_requested, UserRequestsModel.user_id == user_id)).all()]
    # total_api_hits = db.query(UserRequestsModel).filter(and_(cast(UserRequestsModel.created_date, Date) == date_requested, UserRequestsModel.user_id == user_id)).all()

    return record


def get_all_users_for_admin(db: Session):
    records =[z.to_json_for_all_user() for z in db.query(UserModel).all()]

    return records

def get_all_apis_list_with_count(db: Session):

    # result = db.query(UserRequestsModel.endpoint).distinct()
    # result = db.query(func).scalar()
                    #   count(UserRequestsModel.endpoint)).filter_by(UserRequestsModel.statusCode==200).all()
    # result = db.query()
    # result = db.query(UserRequestsModel).distinct(UserRequestsModel.endpoint).count()
    # result = db.query(UserRequestsModel).filter(UserRequestsModel.statusCode.like('%2')).count()
    # result = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint).group_by(UserRequestsModel.endpoint).scalar()

    # goes
    result_goes_files = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint == '/goes/files', or_(UserRequestsModel.statusCode == 201, UserRequestsModel.statusCode == 200)).count()

    result_goes_source_aws_link = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint == '/goes/generate/source-aws-link', or_(UserRequestsModel.statusCode == 201, UserRequestsModel.statusCode == 200)).count()

    result_gen_aws_link_by_filename = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint.like('/goes/generate/aws-link-by-filename/%'), or_(UserRequestsModel.statusCode == 201, UserRequestsModel.statusCode == 200)).count()

    # nexrad

    result_nexrad_files = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint == '/nexrad/files', or_(UserRequestsModel.statusCode == 201, UserRequestsModel.statusCode == 200)).count()

    result_nexrad_source_aws_link = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint == '/nexrad/generate/source-aws-link', or_(UserRequestsModel.statusCode == 201, UserRequestsModel.statusCode == 200)).count()

    result_nexrad_gen_ws_link_by_filename = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint.like('/nexrad/generate/aws-link-by-filename/%'), or_(UserRequestsModel.statusCode == 201, UserRequestsModel.statusCode == 200)).count()

    result_nexrad_map_data = db.query(UserRequestsModel).filter(UserRequestsModel.endpoint == '/nexrad/map-data', or_(UserRequestsModel.statusCode == 201, UserRequestsModel.statusCode == 200)).count()

    # result = "/goes/files"+ result_goes_files + "," + "/goes/generate/source-aws-link" + result_goes_source_aws_link + "," + \
    # "/goes/generate/aws-link-by-filename " + result_gen_aws_link_by_filename + "," + '/nexrad/files' + result_nexrad_source_aws_link + "," + \
    # "/nexrad/generate/aws-link-by-filename " + result_nexrad_gen_ws_link_by_filename + ',' + '/nexrad/map-data ' + result_nexrad_map_data
    
    print(result_goes_files, result_goes_source_aws_link, result_gen_aws_link_by_filename, result_nexrad_source_aws_link, result_nexrad_gen_ws_link_by_filename, result_nexrad_map_data)


    return {
        'success': True,
        '/goes/files': result_goes_files,
        '/goes/generate/source-aws-link': result_goes_source_aws_link,
        '/goes/generate/aws-link-by-filename': result_gen_aws_link_by_filename,
        '/nexrad/files': result_nexrad_files,
        '/nexrad/generate/source-aws-link': result_nexrad_source_aws_link,
        '/nexrad/generate/aws-link-by-filename': result_nexrad_gen_ws_link_by_filename,
        '/nexrad/map-data': result_nexrad_map_data
    }


    # Select endpoint, count(endpoint)
    # From table
    # Where status code == 200/201/..
    # Group by endpoint #,count(endpoint)
