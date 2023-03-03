from pydantic import BaseModel

class GOESAWSFileResponse(BaseModel):
    success:bool
    message:str
    our_bucket_link: str
    source_bucket_link:str
