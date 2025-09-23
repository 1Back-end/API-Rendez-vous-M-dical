from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.user import AddedBySlim
from app.main.schemas.adress import AddressSlim
from app.main.schemas.sexe import Sexe
from app.main.schemas.religion import Religion



class Consultants(BaseModel):
  
    first_name: str
    last_name: str
    phone_number: str
    phone_number_2: str
    email: str 
    titre_uuid: str
    service_hopital_uuid: str
    specialite_uuid: str

    model_config = ConfigDict(from_attributes=True)

class ConsultantsCreate(Consultants):
    pass


class ConsultantsUpdate(BaseModel):
    uuid: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    phone_number_2: Optional[str]
    email: Optional[str] 
    titre_uuid: Optional[str]
    service_hopital_uuid: Optional[str]
    specialite_uuid: Optional[str]



class ConsultantsUpdateStatus(BaseModel):
    uuid: str
    is_active: bool


class ConsultantsDelete(BaseModel):
    uuid: str


class ConsultantsResponse(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    phone_number: str
    phone_number_2: Optional[str]
    email: str 
    titre_uuid: str
    service_hopital_uuid: str
    specialite_uuid: str
    user: AddedBySlim
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ConsultantsResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ConsultantsResponse]

    model_config = ConfigDict(from_attributes=True)


class ConsultantSlim(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    phone_number: str
    phone_number_2: Optional[str]
    email: str
    model_config = ConfigDict(from_attributes=True)

