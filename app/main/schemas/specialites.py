from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.user import AddedBySlim


class Specialites(BaseModel):
    name:str


class SpecialitesCreate(Specialites):
    pass 


class SpecialitesUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    

class SpecialitesDeletes(BaseModel):
    uuid: str

class SpecialitesUpdateStatus(BaseModel):
    uuid: Optional[str]
    status: str



class SpecialitesResponse(BaseModel):
    uuid : str
    name: str
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class SpecialitesResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[SpecialitesResponse]
    model_config = ConfigDict(from_attributes=True)



class SpecialiteSlim(BaseModel):
    uuid:str
    name:str
    model_config = ConfigDict(from_attributes=True)




 
