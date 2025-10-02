from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.adress import AddressSlim
from app.main.schemas.religion import ReligionSlim
from app.main.schemas.sexe import SexeSlim
from app.main.schemas.user import AddedBySlim


class Patient(BaseModel):
    first_name:str
    last_name:str
    phone_number:str
    phone_number_2:Optional[str]
    email:Optional[str]
    address_uuid:str
    sexe_uuid:str
    religion_uuid:str
    is_patient_confidentiel:bool


class PatientCreate(Patient):
    pass


class PatientUpdate(BaseModel):
    uuid:str
    first_name:Optional[str]
    last_name:Optional[str]
    phone_number:Optional[str]
    phone_number_2:Optional[str]
    email:Optional[str]
    address_uuid:Optional[str]
    sexe_uuid:Optional[str]
    religion_uuid:Optional[str]
    is_patient_confidentiel:Optional[bool]


class PatientDelete(BaseModel):
    uuid:str


class PatientUpdateStatus(BaseModel):
    uuid:str
    is_active:bool


class PatientResponse(BaseModel):
    first_name:str
    last_name:str
    phone_number:str
    phone_number_2:Optional[str]
    email:Optional[str]
    address:AddressSlim
    sexe:SexeSlim
    religion:ReligionSlim
    is_patient_confidentiel:bool
    is_active : bool
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)



class PatientResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[PatientResponse]
    model_config = ConfigDict(from_attributes=True)


class PatientSlim(BaseModel):
    first_name:str
    last_name:str
    phone_number:str
    phone_number_2:Optional[str]
    email:Optional[str]
    address:AddressSlim
    sexe:SexeSlim
    religion:ReligionSlim
    is_patient_confidentiel:bool
    model_config = ConfigDict(from_attributes=True)

