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

class CRUDSpecialite(CRUDBase[models.Specialites,schemas.SpecialiteCreate,schemas.SpecialiteUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Specialites).filter(models.Specialites.uuid==uuid,models.Specialites.is_deleted==False).first()


    @classmethod
    def get_by_name(cls,db:Session,name:str):
        return db.query(models.Specialites).filter(models.Specialites.name==name,models.Specialites.is_deleted==False).first()
    
    
    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="specialite-not-found"))
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="specialite-not-found"))
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        db_obj = cls.get_by_uuid(db,uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail="specialite-not-found")
        db_obj.is_active = is_active
        db.commit()

    @classmethod
    def create(cls,db:Session,db_obj:schemas.SpecialiteCreate,added_by:str):
        obj_in = models.Specialites(
            uuid=str(uuid.uuid4()),
            name=db_obj.name,
            added_by = added_by 
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in
    
    @classmethod
    def update(cls,db:Session,obj_in:schemas.SpecialiteUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="specialite-not-found"))
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
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
        record_query = db.query(models.Specialites).filter(models.Specialites.is_deleted==False)
       
        total = record_query.count()
        
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)
        
        return schemas.SpecialiteResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query,
        )

specialite = CRUDSpecialite(models.Specialites)