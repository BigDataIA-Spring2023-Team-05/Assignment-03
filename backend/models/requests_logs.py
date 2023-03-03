from sqlalchemy import Integer, Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import Base
from sqlalchemy.orm import relationship
import datetime


class UserRequestsModel(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=False)
    endpoint = Column(String(255), unique=False)
    statusCode = Column(Integer, nullable=True)
    created_date = Column(DateTime, default= datetime.datetime.utcnow)

    requests = relationship('UserModel', back_populates="user")

    def to_json(self):
        return {
            "user_id": str(self.user_id),
            "endpoint": str(self.endpoint),
            "created_date": self.created_date.strftime("%m/%d/%Y"),
        }
