from pydantic import BaseModel
from typing import List, Optional, Union

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    username: Union[str, None] = None

class User(BaseModel):
    id: Optional[int]
    username: str
    password: str



class GOES(BaseModel):
    station: str 
    year: str
    day: str
    hour: str
    file_name:str

class Nexrad(BaseModel):
    year: str 
    month: str
    day: str
    station_id: str
    file_name:str