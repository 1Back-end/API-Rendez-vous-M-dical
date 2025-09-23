from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


from app.main.schemas.adress import AddressSlim
from app.main.schemas.user import AddedBySlim


class Hopitals(BaseModel):
    name:str
    abbrevation:Optional[str]
    address_uuid:str


class HopitalsCreate(Hopitals):
    pass 


class HopitalsUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    abbrevation: Optional[str]
    address_uuid:str
    

class HopitalsDelete(BaseModel):
    uuid: str

class HopitalsUpdateStatus(BaseModel):
    uuid: Optional[str]
    status: str



class HopitalsResponse(BaseModel):
    uuid : str
    name: str
    abbrevation: Optional[str]
    address : AddressSlim
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class HopitalsResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[HopitalsResponse]
    model_config = ConfigDict(from_attributes=True)