from sqlalchemy.orm import Session

from fastapi import FastAPI
import uvicorn
from routers import user, goes, nexrad, service_plans, profile, admin
from config.db import Base, engine, SessionLocal
from repository import service_plans as servicePlans
from repository import user as UserRepository
from schemas.user import User
from pydantic import BaseModel, Field, EmailStr, validator
from models.user import Role

app =  FastAPI()
db = SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine)
    servicePlans.create(1, 'Free', 10, db= db)
    servicePlans.create(2, 'Gold', 15, db= db)
    servicePlans.create(3, 'Platinum', 20, db= db)
    UserRepository.create(User(username='damg7245', email=EmailStr('rishab1300@gmail.com'), password='spring2023', planId=2), db= db)
    UserRepository.create(User(username='admin', email=EmailStr('mail@heyitsrj.com'), password='spring2023', planId=1, userType = Role.Admin), db= db)

    print("Initialized the db")


@app.on_event("startup")
async def startup():
    app.include_router(user.router)
    app.include_router(goes.router)
    app.include_router(nexrad.router)
    app.include_router(service_plans.router)
    app.include_router(profile.router)
    app.include_router(admin.router)
    
    init_db()


@app.get('/status')
def index():
    return 'Success! APIs are working!'


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

