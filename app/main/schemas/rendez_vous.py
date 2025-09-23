from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime, time
from app.main.schemas.user import AddedBySlim
from app.main.schemas.adress import AddressSlim
from app.main.schemas.sexe import Sexe
from app.main.schemas.religion import Religion
from app.main.schemas.patients import PatientSlim
from app.main.schemas.consultants import ConsultantSlim



class rendez_vous(BaseModel):
  
   consultant_uuid:str
   patient_uuid:str
   date_rendez_vous:datetime
   start_time:datetime
   end_time:datetime
   status:str

class Rendez_VousCreate(rendez_vous):
    pass


class Rendez_VousUpdate(BaseModel):
    uuid: str
    consultant_uuid: Optional[str]
    patient_uuid: Optional[str]
    date_rendez_vous: Optional[datetime]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: Optional[str]


class Rendez_VousUpdateStatus(BaseModel):
    uuid: str
    is_active: bool


class Rendez_VousDelete(BaseModel):
    uuid: str


class Rendez_VousResponse(BaseModel):
    uuid: str
    consultant:ConsultantSlim
    patient:PatientSlim
    date_rendez_vous:datetime
    start_time:time
    end_time:time
    status:str
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class Rendez_VousResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[Rendez_VousResponse]

    model_config = ConfigDict(from_attributes=True)