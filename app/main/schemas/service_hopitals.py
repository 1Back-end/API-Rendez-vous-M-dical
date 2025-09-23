from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.user import AddedBySlim


class ServiceHopital(BaseModel):
    name:str


class ServiceHopitalCreate(ServiceHopital):
    pass 


class ServiceHopitalUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    

class ServiceHopitalDelete(BaseModel):
    uuid: str

class ServiceHopitalUpdateStatus(BaseModel):
    uuid: Optional[str]
    is_active: bool


class ServiceHopitalResponse(BaseModel):
    uuid : str
    name: str
    is_active:bool
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class ServiceHopitalResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ServiceHopitalResponse]
    model_config = ConfigDict(from_attributes=True)



class ServiceHopitalSlim(BaseModel):
    uuid:str
    name:str
    model_config = ConfigDict(from_attributes=True)
 
