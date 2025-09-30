from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SexeBase(BaseModel):
    name: str
    description: Optional[str] = None


class SexeCreate(SexeBase):
    pass

class SexeUpdate(BaseModel):
    uuid:str
    name : Optional[str] = None
    description: Optional[str] = None

class SexeDelete(BaseModel):
    uuid:str

class SexeUpdateStatus(BaseModel):
    uuid:str
    is_active: bool


class SexeResponse(SexeBase):
    uuid:str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class SexeResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[SexeResponse]

    model_config = ConfigDict(from_attributes=True)