from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.user import AddedBySlim

class Specialites(BaseModel):
 name:str
 
class SpecialitesCreate(Specialites):
     pass
 
class SpecialitesUpdate(BaseModel):
    uuid:str
    name:Optional[str]
    
class SpecialitesDelete(BaseModel):
    uuid:str
    
    
class SpecialitesUpdateStatus(BaseModel):
    uuid:str
    is_active:bool

class SpecialitesResponse(BaseModel):
    uuid:str
    name:str
    is_active:bool
    user:AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
    
class SpecilaitesResponseList(BaseModel):
   total :int
   per_page: int
   pages:int
   current_page:int
   data:list[SpecialitesResponse]
   model_config = ConfigDict(from_attributes=True)