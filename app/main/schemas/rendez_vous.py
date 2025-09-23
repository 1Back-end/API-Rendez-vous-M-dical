from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime, time



class RendezVous(BaseModel):
    consultant_uuid:str
    patient_uuid:str
    date_rendez_vous:datetime
    start_time:time
    end_time:time


class RendezVousCreate(RendezVous):
    pass


class RendezVous(BaseModel):
    consultant_uuid:Optional[str]
    patient_uuid:Optional[str]
    date_rendez_vous:Optional[datetime]
    start_time:Optional[time]
    end_time:Optional[time]


    