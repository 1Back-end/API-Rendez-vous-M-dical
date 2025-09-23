from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.user import AddedBySlim

class Titre(BaseModel):
    name: str

class TitreCreate(Titre):
    pass

class TitreUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    
class TitreUpdateStatus(BaseModel):
    uuid: str
    is_active: bool

    
class TitreDelete(BaseModel):
    uuid:str


class TitreResponse(BaseModel):
    uuid: str
    name : str
    user: AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)



class TitreResponseList(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page:int
    data:list[TitreResponse]
    
    model_config = ConfigDict(from_attributes=True)