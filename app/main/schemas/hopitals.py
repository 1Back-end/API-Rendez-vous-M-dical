from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.user import AddedBySlim
from app.main.schemas.adress import AddressSlim


class Hopitals(BaseModel):
    name: str
    address_uuid: str
    abbreviation: str


class HopitalsCreate(Hopitals):
    pass


class HopitalsUpdate(BaseModel):
    uuid: str
    name: Optional[str] = None
    address_uuid: Optional[str] = None
    abbreviation: Optional[str] = None


class HopitalsUpdateStatus(BaseModel):
    uuid: str
    is_active: bool


class HopitalsDelete(BaseModel):
    uuid: str


class HopitalsResponse(BaseModel):
    uuid: str
    name: str
    abbreviation: str
    user: AddedBySlim
    address: AddressSlim
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class HopitalsResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[HopitalsResponse]

    model_config = ConfigDict(from_attributes=True)
