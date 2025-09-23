from typing import Optional, ClassVar
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.user import AddedBySlim
from app.main.schemas.adress import AddressSlim
from app.main.schemas.sexe import Sexe
from app.main.schemas.religion import Religion


class Patient(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    phone_number_2: Optional[str] = None
    email: str
    address_uuid: str
    sexe_uuid: str
    religion_uuid: str
    is_patient_confidentiel: ClassVar[bool] = False
    
    model_config = ConfigDict(from_attributes=True)


class PatientCreate(Patient):
    pass


class PatientUpdate(BaseModel):
    uuid: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    phone_number_2: Optional[str] = None
    email: Optional[str] = None
    address_uuid: Optional[str] = None
    sexe_uuid: Optional[str] = None
    religion_uuid: Optional[str] = None
    is_patient_confidentiel: Optional[bool] = None  # ✅ correction


class PatientUpdateStatus(BaseModel):
    uuid: str
    is_active: bool


class PatientDelete(BaseModel):
    uuid: str


class PatientResponse(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    email: str
    sexe: Sexe
    religion: Religion
    user: AddedBySlim
    address: AddressSlim
    is_patient_confidentiel: bool  # ✅ correction
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PatientResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[PatientResponse]

    model_config = ConfigDict(from_attributes=True)



class PatientSlim(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    email: str
    sexe: Sexe
    religion: Religion
    model_config = ConfigDict(from_attributes=True)
