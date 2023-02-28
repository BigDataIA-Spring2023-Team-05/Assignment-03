from sqlalchemy import Integer, Table, Column
from sqlalchemy.sql.sqltypes import Integer, String 
from config.db import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    api_key = Column(String(255), unique=False, nullable=True)

    # blogs = relationship('Blog', back_populates="creator")

# UserModel = Table(
#     'users', meta,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('username', String(255), unique=True), 
#     Column('email', String(255), unique=True), 
#     Column('password', String(255)),
#     Column('api_key', String(255), unique=True)
# )