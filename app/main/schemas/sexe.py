from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


from app.main.schemas.user import AddedBySlim


class Sexe(BaseModel):
    name:str

    


class SexeCreate(Sexe):
    pass 


class SexeUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    
    
    

class SexeDelete(BaseModel):
    uuid: str


class SexeUpdateStatus(BaseModel):
    uuid: Optional[str]
    is_active: bool




class SexeResponse(BaseModel):
    uuid : str
    name: str
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class SexeResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[SexeResponse]
    model_config = ConfigDict(from_attributes=True)


class SexeSlim(BaseModel):
    uuid : str
    name:str
    model_config = ConfigDict(from_attributes=True)