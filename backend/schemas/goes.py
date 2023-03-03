from pydantic import BaseModel

class GOESAWSFileResponse(BaseModel):
    success:bool
    message:str
    bucket_link: str