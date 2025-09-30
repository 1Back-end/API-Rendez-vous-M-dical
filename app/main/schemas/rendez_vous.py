from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime, time


<<<<<<< HEAD
class RendezVousBase(BaseModel):
=======

class RendezVous(BaseModel):
>>>>>>> 3ea90b8c53f13b8391ee1d89cfde4eaf50aeef82
    consultant_uuid:str
    patient_uuid:str
    date_rendez_vous:datetime
    start_time:time
    end_time:time

<<<<<<< HEAD
class RendezVousCreate(RendezVousBase):
    pass

class RendezVousUpdate(BaseModel):
=======

class RendezVousCreate(RendezVous):
    pass


class RendezVous(BaseModel):
>>>>>>> 3ea90b8c53f13b8391ee1d89cfde4eaf50aeef82
    consultant_uuid:Optional[str]
    patient_uuid:Optional[str]
    date_rendez_vous:Optional[datetime]
    start_time:Optional[time]
    end_time:Optional[time]

<<<<<<< HEAD
class RendezVousDelete(BaseModel):
    uuid:str

class RendezVousUpdateStatus(BaseModel):
    uuid:Optional[str]
    status:str

class RendezVousResponse(BaseModel):
    consultant : ConsultantSlim
    patient:PatientSlim
    date_rendez_vous: datetime
    start_time: time
    end_time: time
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class RendezVousResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[RendezVousResponse]

    model_config = ConfigDict(from_attributes=True)


=======

    
>>>>>>> 3ea90b8c53f13b8391ee1d89cfde4eaf50aeef82
