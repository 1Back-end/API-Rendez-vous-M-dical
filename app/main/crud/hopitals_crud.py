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

class CRUDHopitals(CRUDBase[models.Hopitals,schemas.HopitalsCreate,schemas.HopitalsUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Hopitals).filter(models.Hopitals.uuid==uuid,models.Hopitals.is_deleted==False).first()
    
    @classmethod
    def get_by_name(cls,db:Session,name:str):
        return db.query(models.Hopitals).filter(models.Hopitals.name==name,models.Hopitals.is_deleted==False).first()
    
    @classmethod
    def get_by_address(cls,db:Session,address_uuid:str):
        return db.query(models.Hopitals).filter(models.Hopitals.address_uuid==address_uuid,models.Hopitals.is_deleted==False).all()
    
    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj=cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="hopitals-not-found"))
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db==db,uuid==uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="hopitals-not-found"))
        db_obj.is_deleted=True
        db.commit()

    @classmethod
    def create(cls,db:Session,obj_in:schemas.HopitalsCreate,added_by:str):
        db_obj=models.Hopitals(
            uuid=str(uuid.uuid4()),
            name = obj_in.name,
            address_uuid=obj_in.address_uuid,
            abbreviation = obj_in.abbreviation,
            added_by = added_by

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @classmethod
    def update(cls,db:Session,obj_in:schemas.HopitalsUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="hopitals-not-found")
        db_obj.name = obj_in.name if obj_in.name else db_obj.name,
        db_obj.address_uuid = obj_in.address_uuid if obj_in.address_uuid else db_obj.address_uuid,
        db_obj.abbreviation = obj_in if obj_in.abbreviation else db_obj.abbreviation,
        db_obj.added_by = added_by

        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def get_many(
        cls,
        db:Session,
        page: int = 1,
        per_page: int = 25,
    ):
        record_query = db.query(models.Hopitals).filter(models.Hopitals.is_deleted==False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)
        
        return schemas.HopitalsResponseList(
            total = total,
            pages = math.ceil(total / per_page),
            per_page = per_page,
            current_page = page,
            data = record_query
        )
    
    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="hopitals-not-found"))
        db_obj.is_active = is_active
        db.commit()



        
hopitals = CRUDHopitals(models.Hopitals)
