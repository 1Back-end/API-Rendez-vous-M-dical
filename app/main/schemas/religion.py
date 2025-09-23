from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.user import AddedBySlim


class Religion(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class ReligionCreate(Religion):
    pass


class ReligionUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    
    

class ReligionUpdateStatus(BaseModel):
    uuid: str
    is_active: bool


class ReligionDelete(BaseModel):
    uuid:str


class ReligionResponse(BaseModel):
    uuid: str
    name : str
    user: AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)



class ReligionResponseList(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page:int
    data:list[ReligionResponse]
    
    model_config = ConfigDict(from_attributes=True)