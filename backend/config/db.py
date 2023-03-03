from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = 'root'
DB_PASSWORD = '123456789'
DB_HOST = 'dbsql'
DB_PORT = '3306'
DB_NAME = 'assignment_03'

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# try: 
#     engine.execute('CREATE DATABASE assignment_03')
# except Exception as db_exc:
#     print(db_exc)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()