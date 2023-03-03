from fastapi import APIRouter, status, HTTPException, Response, Depends, Request
from schemas.schemas import User, GOES, TokenData
from middleware.oauth2 import get_current_user
from awscloud.s3 import main as aws
import re
from config import db
from middleware.requests_logs import TimedRoute
from fastapi.responses import JSONResponse
from schemas.index import GOESAWSFileResponse, UserPlan
from repository.requests_logs import get_user_specific_api_rate_limit
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/goes',
    tags=['GOES 18'],
    route_class= TimedRoute
)
get_db = db.get_db

@router.get('/files')
def get_all_goes_file(station: str, year: str, day: str, hour: str, response: Response, get_current_user: TokenData = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit)):
    # Code to retrieve from filename form SQL Lite DB.
    if is_limit is True:
        result = aws.get_all_geos_file_name_by_filter(station=station, year=year, day=day, hour=hour)

        return {
            'success':True,
            'all_files': result
        }
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )

@router.post('/generate/source-aws-link', status_code=status.HTTP_201_CREATED)
def generate_aws_link(request: GOES, get_current_user: TokenData = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit)):
    if is_limit is True:
        result = aws.get_aws_link_by_filename(request.file_name)
        
        if(result == None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested file does not exists!")

        return {
            'success':True,
            'message':'link generated',
            'goes_link':result
        }
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )


@router.post('/generate/aws-link-by-filename/{filename}', 
             status_code=status.HTTP_201_CREATED,
             response_model=GOESAWSFileResponse,
             responses={
                404: {'success': False, "message": "Requested file does not exists in GOES S3 Bucket!"},
                status.HTTP_400_BAD_REQUEST: {'success': False, "message": "Invalid file name"},
            }
        )
def generate_aws_link_by_filename(filename, request: Request, get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db), is_limit: bool = Depends(get_user_specific_api_rate_limit)):
    
    if is_limit is True:
        regex = re.compile(r'(OR)_(ABI)-(L\d+b)-(Rad[A-Z]?)-([A-Z]\dC\d{2})_(G\d+)_(s\d{14})_(e\d{14})_(c\d{14}).nc')
        match = regex.match(filename)
        if not match:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'success': False, 
                    "message": "Invalid file name"
                }
            )
        
        result = aws.get_our_aws_link_by_filename(filename= filename)

        if(result == None):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'success': False, 
                    "message": "Requested file does not exists in GOES S3 Bucket!"
                }
            )
        
        return GOESAWSFileResponse(success = True, message= 'original bucket link', our_bucket_link= result[0], source_bucket_link= result[1])
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )