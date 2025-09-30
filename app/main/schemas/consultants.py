from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas.service_hopitals import ServiceHopitalSlim
from app.main.schemas.specialites import SpecialiteSlim
from app.main.schemas.titres import TitreSlim
from app.main.schemas.user import AddedBySlim


class Consultant(BaseModel):
    first_name:str
    last_name:str
    phone_number:str
    phone_number_2:Optional[str]
    email:str
    titre_uuid:str
    service_hopital_uuid:str
    specialite_uuid:str


class ConsultantCreate(Consultant):
    pass


class ConsultantUpdate(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    phone_number:Optional[str]
    phone_number_2:Optional[str]
    email:Optional[str]
    titre_uuid:Optional[str]
    service_hopital_uuid:Optional[str]
    specialite_uuid:Optional[str]


class ConsultantDelete(BaseModel):
    uuid:str


class ConsultantUpdateStatus(BaseModel):
    uuid : str
    is_active : bool


class ConsultantResponse(BaseModel):
    uuid:str
    first_name:str
    last_name:str
    phone_number:str
    phone_number_2:Optional[str]
    email:str
    titre:TitreSlim
    service_hopital:ServiceHopitalSlim
    specialite:SpecialiteSlim
    is_active : bool
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class ConsultantResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ConsultantResponse]
    model_config = ConfigDict(from_attributes=True)




class ConsultantSlim(BaseModel):
    uuid:str
    first_name:str
    last_name:str
    phone_number:str
    phone_number_2:Optional[str]
    email:str
    titre:TitreSlim
    service_hopital:ServiceHopitalSlim
    specialite:SpecialiteSlim
    model_config = ConfigDict(from_attributes=True)



