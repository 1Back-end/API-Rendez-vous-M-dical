from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.address import AddressSlim
from app.main.schemas.user import AddedBySlim

class Hopitals(BaseModel):
 name:str
 abbreviation:str
 address_uuid:str
 
 
class HopitalsCreate(Hopitals):
     pass
 
class HopitalsUpdate(BaseModel):
    uuid:str
    name:Optional[str]
    abbrevation:Optional[str]
    address_uuid:Optional[str]
    
class HopitalsDelete(BaseModel):
    uuid:str
    
    
class HopitalsUpdateStatus(BaseModel):
    uuid:str
    is_active:bool

class HopitalsResponse(BaseModel):
    uuid:str
    name:str
    abbrevation:str
    is_active:bool
    user:AddedBySlim
    address:AddressSlim
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
    
class HospitalsResponseList(BaseModel):
   total :int
   per_page: int
   pages:int
   current_page:int
   data:list[HopitalsResponse]
   model_config = ConfigDict(from_attributes=True)