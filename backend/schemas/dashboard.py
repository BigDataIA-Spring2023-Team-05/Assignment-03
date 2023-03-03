from pydantic import BaseModel, Field
from . service_plan import Plan

class UserDashboardResponse(BaseModel):
    plan: Plan
    total_api_hits_in_hr: int = Field(
        default=0
    )
    total_successful_api_hits_in_hr: int = Field(
        default= 0
    )
    total_failed_api_hits_in_hr: int = Field(
        default= 0
    )


