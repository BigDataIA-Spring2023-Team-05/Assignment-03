from fastapi import FastAPI, status, Response, HTTPException
import uvicorn
from routers import user_v2
from config.db import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Initialized the db")


app =  FastAPI()
init_db()

app.include_router(user_v2.router)
# app.include_router(goes.router)
# app.include_router(nexrad.router)

@app.get('/status')
def index():
    return 'Success! APIs are working!'


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

 