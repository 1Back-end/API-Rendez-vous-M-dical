from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.user import AddedBySlim



class ServiceHopitals(BaseModel):
    name: str
   

class ServiceHopitalsCreate(ServiceHopitals):
    pass

class ServiceHopitalsUpdate(BaseModel):
    uuid: str
    name: Optional[str]=None

    
class ServiceHopitalsUpdateStatus(BaseModel):
    uuid: str
    is_active: bool

    
class ServiceHopitalsDelete(BaseModel):
    uuid:str


class ServiceHopitalsResponse(BaseModel):
    uuid: str
    name : str
    user: AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)



class ServiceHopitalsResponseList(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page:int
    data:list[ServiceHopitalsResponse]

    model_config = ConfigDict(from_attributes=True)