from sqlalchemy import Integer, Table, Column, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import Base
from sqlalchemy.orm import relationship
import datetime
import enum

class Role(enum.Enum):
    Admin = 1
    User = 2

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    apiKey = Column(String(255), unique=False, nullable=True)
    planId = Column(Integer, ForeignKey('servicePlans.id'), unique=False, nullable= False, default= 1)
    created_date = Column(DateTime, default= datetime.datetime.utcnow)
    userType = Column(Enum(Role), default=Role.User)


    user = relationship("UserRequestsModel", back_populates="requests")
    plan = relationship("ServicePlanModel", back_populates="user")

    # user_plans = relationship("ServicePlanModel", back_populates="plans")
    def to_json_for_all_user(self):
        return {
            "id": str(self.id),
            "username": str(self.username)
        }