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
from app.main.core.security import generate_password, get_password_hash, verify_password
from app.main.core.mail import send_account_creation_email  # Envoi mail à la création de compte

class CRUDconsultants(CRUDBase[models.Consultants,schemas.ConsultantsCreate,schemas.ConsultantsUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Consultants).filter(models.Consultants.uuid==uuid,models.Consultants.is_deleted==False).first()
    

    @classmethod
    def get_by_phone_number(cls,db:Session,phone_number:str):
        return db.query(models.Consultants).filter(models.Consultants.phone_number==phone_number,models.Consultants.is_deleted==False).first()

    @classmethod
    def get_by_phone_number_2(cls,db:Session,phone_number_2:str):
        return db.query(models.Consultants).filter(models.Consultants.phone_number_2==phone_number_2,models.Consultants.is_deleted==False).first()

    @classmethod
    def get_by_email(cls,db:Session,email:str):
        return db.query(models.Consultants).filter(models.Consultants.email==email,models.Consultants.is_deleted==False).first()

    @classmethod
    def get_by_titre_uuid(cls,db:Session,titre_uuid:str):
        return db.query(models.Consultants).filter(models.Consultants.titre_uuid==titre_uuid,models.Consultants.is_deleted==False).first()

    @classmethod
    def get_by_service_hopital_uuid(cls,db:Session,service_hopital_uuid:str):
        return db.query(models.Consultants).filter(models.Consultants.service_hopital_uuid==service_hopital_uuid,models.Consultants.is_deleted==False).first()
    
    @classmethod
    def get_by_specialite_uuid(cls,db:Session,specialite_uuid:str):
        return db.query(models.Consultants).filter(models.Consultants.specialite_uuid==specialite_uuid,models.Consultants.is_deleted==False).first()

    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj=cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="consultant-not-found")
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db==db,uuid==uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="consultant-not-found")
        db_obj.is_deleted=True
        db.commit()

    @classmethod
    def create(cls,db:Session,obj_in:schemas.ConsultantsCreate,added_by:str):

        password: str = generate_password(8, 8)
        print(f"User password: {password}")

        common_uuid = str(uuid.uuid4())

        db_obj=models.Consultants(
            uuid=common_uuid,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            phone_number=obj_in.phone_number,
            phone_number_2=obj_in.phone_number_2,
            email=obj_in.email,
            titre_uuid=obj_in.titre_uuid,
            service_hopital_uuid = obj_in.service_hopital_uuid,
            specialite_uuid = obj_in.specialite_uuid,
            added_by = added_by,

        )
        db.add(db_obj)

        new_user = models.User(
            uuid=common_uuid,
            email = obj_in.email,
            phone_number = obj_in.phone_number,
            first_name = obj_in.first_name,
            last_name = obj_in.last_name,
            password_hash = get_password_hash(password),
            role = models.UserRole.CONSULTANT
        )
        db.add(new_user)

        db.commit()

        db.refresh(db_obj)

        send_account_creation_email(
            email_to=obj_in.email,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            password=password
        )
        return db_obj
    
    @classmethod
    def update(cls,db:Session,obj_in:schemas.ConsultantsUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="patient-not-found")
        db_obj.first_name = obj_in.first_name if obj_in.first_name else db_obj.first_name,
        db_obj.last_name = obj_in.last_name if obj_in.last_name else db_obj.last_name,
        db_obj.phone_number = obj_in.phone_number if obj_in.phone_number else db_obj.phone_number,
        db_obj.phone_number_2 = obj_in.phone_number_2 if obj_in.phone_number_2 else db_obj.phone_number_2,
        db_obj.email = obj_in.email if obj_in.email else db_obj.email,
        db_obj.titre_uuid = obj_in if obj_in.titre_uuid else db_obj.titre_uuid,
        db_obj.service_hopital_uuid = obj_in if obj_in.service_hopital_uuid else db_obj.service_hopital_uuid,
        db_obj.specialite_uuid = obj_in if obj_in.specialite_uuid else db_obj.specialite_uuid,
        db_obj.added_by = added_by
        
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="consultant-not-found"))
        db_obj.is_active = is_active
        db.commit()

    @classmethod
    def get_many(
        cls,
        db:Session,
        page: int = 1,
        per_page: int = 25,
    ):
        record_query = db.query(models.Consultants).filter(models.Consultants.is_deleted==False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)
        return schemas.ConsultantsResponseList(
            total = total,
            pages = math.ceil(total / per_page),
            per_page = per_page,
            current_page = page,
            data = record_query
        )



        
consultants = CRUDconsultants(models.Consultants)