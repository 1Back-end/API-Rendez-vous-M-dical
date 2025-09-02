from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.user import AddedBySlim


class Sexe(BaseModel):
    name: str


class SexeCreate(Sexe):
    pass
   


class SexeUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    


class SexeDelete(BaseModel):
    uuid: str
   

class SexeUpdateStatus(BaseModel):
    uuid:str
    is_active:bool


class SexeResponse(BaseModel):
    uuid: str
    name: str
    is_active:bool
    user:AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class SexeResponseList(BaseModel):
    total: int
    per_page: int
    pages: int
    current_page: int
    data: list[SexeResponse]
    model_config = ConfigDict(from_attributes=True)
