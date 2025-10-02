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

class CRUDPatient(CRUDBase[models.Patient,schemas.PatientCreate,schemas.PatientUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Patient).filter(models.Patient.uuid==uuid,models.Patient.is_deleted==False).first()
    
    @classmethod
    def get_by_phone_number(cls,db:Session,phone_number:str):
        return db.query(models.Patient).filter(models.Patient.phone_number==phone_number,models.Patient.is_deleted==False).first()
    
    @classmethod
    def get_by_email(cls,db:Session,email:str):
        return db.query(models.Patient).filter(models.Patient.email==email,models.Patient.is_deleted==False).first()
    
    @classmethod
    def get_by_phone_number2(cls,db:Session,phone_number_2:str):
        return db.query(models.Patient).filter(models.Patient.phone_number_2==phone_number_2,models.Patient.is_deleted==False).first()
    
    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="patient-not-found")
        db_obj.is_active = is_active
        db.commit()
    
    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)  
        if not db_obj:
             raise HTTPException(status_code=404,detail=__(key="patient-not-found"))
        db.delete(db_obj)
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="patient-not-found")
        db_obj.is_deleted=True
        db.commit()


    @classmethod
    def create(cls,db:Session, obj_in:schemas.PatientCreate,added_by:str):
        db_obj = models.Patient(
            uuid = str(uuid.uuid4()),
            first_name = obj_in.first_name,
            last_name = obj_in.last_name,
            phone_number = obj_in.phone_number,
            phone_number_2 = obj_in.phone_number_2,
            email = obj_in.email,
            address_uuid = obj_in.address_uuid,
            sexe_uuid = obj_in.sexe_uuid,
            religion_uuid = obj_in.religion_uuid,
            is_patient_confidentiel = obj_in.is_patient_confidentiel,
            added_by = added_by   
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,obj_in:schemas.PatientUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="patient-not-found")
        db_obj.first_name = obj_in.first_name if obj_in.first_name else db_obj.first_name
        db_obj.last_name = obj_in.last_name if obj_in.last_name else db_obj.last_name
        db_obj.phone_number = obj_in.phone_number if obj_in.phone_number else db_obj.phone_number
        db_obj.phone_number_2 = obj_in.phone_number_2 if obj_in.phone_number_2 else db_obj.phone_number_2
        db_obj.email = obj_in.email if obj_in.email else db_obj.email
        db_obj.address_uuid = obj_in.address_uuid if obj_in.address_uuid else db_obj.address_uuid
        db_obj.sexe_uuid = obj_in.sexe_uuid if obj_in.sexe_uuid else db_obj.sexe_uuid
        db_obj.religion_uuid = obj_in.religion_uuid if obj_in.religion_uuid else db_obj.religion_uuid
        db_obj.is_patient_confidentiel = obj_in.is_patient_confidentiel if obj_in.is_patient_confidentiel else db_obj.is_patient_confidentiel
        db_obj.added_by = added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def get_many(
        cls,
        db: Session,
        page: int = 1,
        per_page: int = 25,
        order: Optional[str] = None,
        order_field: Optional[str] = None,
        keyword: Optional[str]=None,
    ):
        
        record_query = db.query(models.Patient).filter(models.Patient.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Patient.first_name.ilike(f'%{keyword}%'),
                    models.Patient.last_name.ilike(f'%{keyword}%'),
                    models.Patient.phone_number.ilike(f'%{keyword}%'),
                    models.Patient.phone_number_2.ilike(f'%{keyword}%'),
                    models.Patient.email.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Patient, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Patient, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Patient, order_field).desc())

        total= record_query.count()

        record_query = record_query. offset((page - 1 ) * per_page). limit(per_page)

        return schemas.PatientResponseList(
            total= total,
            pages= math.ceil(total / per_page),
            per_page=per_page,
            current_page= page,
            data= record_query,

        )


patient = CRUDPatient(models.Patient) 