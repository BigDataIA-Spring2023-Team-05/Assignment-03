from fastapi import APIRouter, status, HTTPException, Response, Depends
from schemas.index import User, Nexrad
from middleware.oauth2 import get_current_user
from awscloud.s3 import nexrad_main as aws
from schemas.schemas import TokenData
from data.mapdata import MapData
import re
from fastapi.responses import JSONResponse
from repository.requests_logs import get_user_specific_api_rate_limit
from sqlalchemy.orm import Session
from middleware.requests_logs import TimedRoute

mapData = MapData()

router = APIRouter(
    prefix='/nexrad',
    tags=['NEXRAD 18'],
    route_class= TimedRoute
)


@router.get('/files')
def get_all_nexrad_file(stationId: str, year: str, day: str, month: str, response: Response, get_current_user: TokenData = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit)):
    # Code to retrieve from filename form SQL Lite DB.
    if is_limit is True:
        result = aws.get_all_nexrad_file_name_by_filter(station=stationId, year=year, day=day, month=month)

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
def generate_aws_link(request: Nexrad, get_current_user:User = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit)):
    
    if is_limit is True:
        result = aws.get_nexrad_aws_link_by_filename(request.file_name)
        
        if(result == None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested file does not exists!")


        return {
            'success':True,
            'message':'link generated',
            'nexrad_link':result
        }
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )


@router.post('/generate/aws-link-by-filename/{filename}', status_code=status.HTTP_201_CREATED)
def generate_aws_link_by_filename(filename, get_current_user:TokenData = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit)):
    if is_limit is True:
        regex = re.compile(r'K[A-Z]{3}[0-9]{8}_[0-9]{6}(_V06_MDM)?')
        match = regex.match(filename)

        if not match:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file name!")
        
        result = aws.get_our_aws_link_by_filename(filename=filename)

        if(result == None):
            return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'success': False, 
                        "message": "Requested file does not exists in GOES S3 Bucket!"
                    }
                )    
        
        return {
            'success':True,
            'message':'original bucket link',
            'source_bucket_link':result[1],
            'our_bucket_link': result[0] 
        }
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )


@router.get('/map-data', status_code=status.HTTP_200_OK)
def get_map_data(get_current_user:User = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit)):
    if is_limit is True:
        return mapData.get_data_for_map()
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )
