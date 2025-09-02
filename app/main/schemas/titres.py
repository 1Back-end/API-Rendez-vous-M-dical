from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.user import AddedBySlim

class Titre(BaseModel):
 name:str
 
class TitreCreate(Titre):
     pass
 
class TitreUpdate(BaseModel):
    uuid:str
    name:Optional[str]
    
class TitreDelete(BaseModel):
    uuid:str
    

class TitreUpdateStatus(BaseModel):
    uuid:str
    is_active:bool

class TitreResponse(BaseModel):
    uuid:str
    name:str
    is_active:bool
    user:AddedBySlim
    model_config = ConfigDict(from_attributes=True)
    
class TitreResponseList(BaseModel):
   total :int
   per_page: int
   pages:int
   current_page:int
   data:list[TitreResponse]
   model_config = ConfigDict(from_attributes=True)