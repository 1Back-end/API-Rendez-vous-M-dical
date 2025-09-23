from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.user import AddedBySlim



class Specialite(BaseModel):
    name: str
   

class SpecialiteCreate(Specialite):
    pass

class SpecialiteUpdate(BaseModel):
    uuid: str
    name: Optional[str]=None

    
class SpecialiteUpdateStatus(BaseModel):
    uuid: str
    is_active: bool

    
class SpecialiteDelete(BaseModel):
    uuid:str


class SpecialiteResponse(BaseModel):
    uuid: str
    name : str
    user: AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)



class SpecialiteResponseList(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page:int
    data:list[SpecialiteResponse]

    model_config = ConfigDict(from_attributes=True)