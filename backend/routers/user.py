from fastapi import APIRouter, status, HTTPException, Response, Depends
from utils import hashing, JWT_token
from schemas.index import User, UserResponse, LoginResponse, ForgotPassword, VerifyForgotPassword, PasswordResetRequest
from sqlalchemy.orm import Session
from config import db
from repository import user
from fastapi.security import OAuth2PasswordRequestForm
from utils.redis import register_otp, verify_otp
import random
from awscloud.ses.main import Email
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/user',
    tags=['User']
)

get_db = db.get_db


@router.post('/sign-up', status_code=status.HTTP_201_CREATED, response_model= UserResponse)
def sign_up_user(request: User, db: Session = Depends(get_db)):

    if request.planId not in [1, 2, 3]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please sepcify plan id")
    
    result = user.create(request = request, db = db)

    if result is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")
    else:
        return result



@router.post('/login', status_code=status.HTTP_200_OK, response_model= LoginResponse)
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = user.find_user(request.username, request.password, db = db)

    if result is HTTPException:
        return result
    
    return result


@router.post('/forgot-password', status_code=status.HTTP_200_OK,
             responses={
                200:{
                    'success': True, 
                    'message': "OTP verified"
                }
             })
def send_reset_otp_to_user(request:ForgotPassword, db: Session = Depends(get_db)):
    result = user.find_user_by_email(request.email, db= db)

    if result is HTTPException:
        return result
    
    otp = random.randint(111111,999999)
    register_otp(result.email, otp= otp)
    Email().send_html_email(str(result.email), otp= otp)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True, 
            "message": "Password reset OTP sent on email"
        }
    )

# @router.post('/verify-otp', status_code=status.HTTP_200_OK)
# def verify_OTP(request: VerifyForgotPassword, db:Session = Depends(get_db)):
#     otp_stored = verify_otp(request.email)

#     if otp_stored is None:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={
#                 'success': False, 
#                 'message': "OTP expired"
#                 }
#         )

#     if otp_stored == str(request.otp):
#         return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={
#             'success': True, 
#             'message': "OTP verified",
#             'email': request.email
#             }
#         )
#     else:
#         return JSONResponse(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         content={
#             'success': False, 
#             "message": "Unable to verify OTP."
#             }
#         )


@router.post('/reset-password', status_code=status.HTTP_201_CREATED)
def change_to_new_password(request:PasswordResetRequest, db: Session = Depends(get_db)):

    otp_stored = verify_otp(request.email)
    
    if otp_stored is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'success': False, 
                    'message': "OTP expired"
                    }
            )

    if otp_stored != str(request.otp):
        return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            'success': False, 
            "message": "Unable to verify OTP."
            }
        )

    result = user.change_user_password_to_new(request.email, request.new_password, db= db)

    if request.new_password != request.confirm_password:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'success': False, 
            "message": "New password and confirm password don't match"
            }
        )

    if result is None:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'success': False, 
            "message": "Unable to find password"
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'success': True, 
            "message": "Password reset successful!"
            }
        )