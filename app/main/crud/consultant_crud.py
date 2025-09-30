import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas

class CRUDConsultant(CRUDBase[models.Consultants,schemas.ConsultantCreate,schemas.ConsultantUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Consultants).filter(models.Consultants.uuid==uuid,models.Consultants.is_deleted==False).first()
    
    @classmethod
    def get_by_email(cls,db:Session,email:str):
        return db.query(models.Consultants).filter(models.Consultants.email==email,models.Consultants.is_deleted==False).first()
        
    @classmethod
    def get_by_phone_number(cls,db:Session,phone_number:str):
        return db.query(models.Consultants).filter(models.Consultants.phone_number==phone_number,models.Consultants.is_deleted==False).first()    
    
    @classmethod
    def get_by_phone_number2(cls,db:Session,phone_number2:str):
        return db.query(models.Consultants).filter(models.Consultants.phone_number_2==phone_number2,models.Consultants.is_deleted==False).first()
    

    @classmethod
    def create(cls,db:Session,obj_in:schemas.ConsultantCreate,added_by:str):
        db_obj=models.Consultants(
            uuid=str(uuid.uuid4()),
            first_name = obj_in.first_name,
            last_name = obj_in.last_name,
            phone_number_2 = obj_in.phone_number_2,
            email = obj_in.email,
            titre_uuid = obj_in.titre_uuid,
            service_hopital_uuid = obj_in.service_hopital_uuid,
            specialite_uuid = obj_in.specialite_uuid,
            added_by = added_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    



    @classmethod
    def delete(cls,db:Session,uuid:str):
        obj_in = cls.get_by_uuid(db=db,uuid=uuid)
        if not obj_in:
            raise HTTPException(status_code=404,detail=__(key="consultant-not-fount"))
