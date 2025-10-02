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
        db.delete(obj_in)
        db.commit()
    
    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        obj_in =cls.get_by_uuid(db=db,uuid=uuid)
        if not obj_in:
            raise HTTPException(status_code=404,detail=__(key="consultant-not-fount"))
        obj_in.is_deleted = False
        db.commit()



    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="consultant-not-found")
        db_obj.is_active = is_active
        db.commit()


    @classmethod
    def update(cls,db:Session,obj_in:schemas.ConsultantUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="consultant-not-found")
        db_obj.first_name = obj_in.first_name if obj_in.first_name else db_obj.first_name
        db_obj.last_name = obj_in.last_name if obj_in.last_name else db_obj.last_name
        db_obj.phone_number = obj_in.phone_number if obj_in.phone_number else db_obj.phone_number
        db_obj.phone_number2 = obj_in.phone_number2 if obj_in.phone_number2 else db_obj.phone_number2
        db_obj.email = obj_in.email if obj_in.email else db_obj.email
        db_obj.titre_uuid = obj_in.titre_uuid if obj_in.titre_uuid else db_obj.titre_uuid
        db_obj.service_hopital_uuid = obj_in.service_hopital_uuid if obj_in.service_hopital_uuid else db_obj.service_hopital_uuid
        db_obj.specialite_uuid = obj_in.specialite_uuid if obj_in.specialite_uuid else db_obj.specialite_uuid
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
        record_query = db.query(models.Consultants).filter( models.Consultants.is_deleted == False)
        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Consultants.first_name.ilike(f'%{keyword}%'),
                    models.Consultants.last_name.ilike(f'%{keyword}%'),
                    models.Consultants.email.ilike(f'%{keyword}%'),
                    models.Consultants.phone_number.ilike(f'%{keyword}%'),
                    models.Consultants.phone_number_2.ilike(f'%{keyword}%'),
                )
            )

        if order and order_field and hasattr(models.Consultants, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Consultants, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Consultants, order_field).desc())

        total = record_query.count() 
        # Pagination avec offset et limit
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        # Retourne une réponse paginée avec total, pages, page actuelle, nombre par page et liste des données
        return schemas.ConsultantResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query,
        )


        

    

        
