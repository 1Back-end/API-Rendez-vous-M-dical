from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

<<<<<<< HEAD

class SexeBase(BaseModel):
    name: str
    description: Optional[str] = None


class SexeCreate(SexeBase):
    pass

class SexeUpdate(BaseModel):
    uuid:str
    name : Optional[str] = None
    description: Optional[str] = None

class SexeDelete(BaseModel):
    uuid:str

class SexeUpdateStatus(BaseModel):
    uuid:str
    is_active: bool


class SexeResponse(SexeBase):
    uuid:str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
=======
<<<<<<< HEAD

=======
>>>>>>> 79ec58cd0c1a2119c875d4d68ce9c032b285010a
from app.main.schemas.user import AddedBySlim


class Sexe(BaseModel):
<<<<<<< HEAD
    name:str

    


class SexeCreate(Sexe):
    pass 
=======
    name: str


class SexeCreate(Sexe):
    pass
   
>>>>>>> 79ec58cd0c1a2119c875d4d68ce9c032b285010a


class SexeUpdate(BaseModel):
    uuid: str
    name: Optional[str]
    
<<<<<<< HEAD
    
    

class SexeDelete(BaseModel):
    uuid: str


class SexeUpdateStatus(BaseModel):
    uuid: Optional[str]
    is_active: bool




class SexeResponse(BaseModel):
    uuid : str
    name: str
    user : AddedBySlim 
    created_at:datetime
    updated_at: Optional[datetime]
>>>>>>> 3ea90b8c53f13b8391ee1d89cfde4eaf50aeef82
    model_config = ConfigDict(from_attributes=True)

class SexeResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
<<<<<<< HEAD
    current_page:int
    data: list[SexeResponse]

    model_config = ConfigDict(from_attributes=True)
=======
    current_page: int
    data: list[SexeResponse]
    model_config = ConfigDict(from_attributes=True)


class SexeSlim(BaseModel):
    uuid : str
    name:str
    model_config = ConfigDict(from_attributes=True)
=======


class SexeDelete(BaseModel):
    uuid: str
   

class SexeUpdateStatus(BaseModel):
    uuid:str
    is_active:bool


class SexeResponse(BaseModel):
    uuid: str
    name: str
    is_active:bool
    user:AddedBySlim
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class SexeResponseList(BaseModel):
    total: int
    per_page: int
    pages: int
    current_page: int
    data: list[SexeResponse]
    model_config = ConfigDict(from_attributes=True)
>>>>>>> 79ec58cd0c1a2119c875d4d68ce9c032b285010a
>>>>>>> 3ea90b8c53f13b8391ee1d89cfde4eaf50aeef82
