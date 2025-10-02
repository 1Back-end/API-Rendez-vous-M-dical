from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime, time


class RendezVousBase(BaseModel):

class Rendez_Vous(BaseModel):
    consultant_uuid:str
    patient_uuid:str
    date_rendez_vous:datetime
    start_time:time
    end_time:time


class Rendez_VousCreate(Rendez_Vous):
    pass


class Rendez_VousUpdate(BaseModel):
    uuid:str
    consultant_uuid:Optional[str]
    patient_uuid:Optional[str]
    date_rendez_vous:Optional[datetime]
    start_time:Optional[time]
    end_time:Optional[time]


class Rendez_VousDelete(BaseModel):
    uuid:str


class Rendez_VousUpdateStatus(BaseModel):
    uuid:str
    is_active:bool


class Rendez_VousResponse(BaseModel):
    consultant_uuid:str
    patient_uuid:str
    date_rendez_vous:datetime
    start_time:time
    end_time:time
    is_active : bool
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)



class Rendez_VousResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[Rendez_VousResponse]
    model_config = ConfigDict(from_attributes=True)


class Rendez_VousSlim(BaseModel):
    consultant_uuid:str
    patient_uuid:str
    date_rendez_vous:datetime
    start_time:time
    end_time:time
    model_config = ConfigDict(from_attributes=True)    


    