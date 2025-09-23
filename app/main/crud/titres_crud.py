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

class CRUDTitre(CRUDBase[models.Titre,schemas.TitreCreate,schemas.TitreUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Titre).filter(models.Titre.uuid==uuid,models.Titre.is_deleted==False).first()
    

    @classmethod
    def get_by_name(cls,db:Session,name:str):
        return db.query(models.Titre).filter(models.Titre.name==name,models.Titre.is_deleted==False).first()
    
    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)  
        if not db_obj:
             raise HTTPException(status_code=404,detail=__(key="titre-not-found"))
        db.delete(db_obj)
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="titre-not-found")
        db_obj.is_deleted=True
        db.commit()

    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="titre-not-found")
        db_obj.is_active = is_active
        db.commit()

    
    @classmethod
    def create(cls,db:Session, obj_in:schemas.TitreCreate,added_by:str):
        db_obj = models.Titre(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            added_by = added_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,obj_in:schemas.TitreUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="Titre-not-found")
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
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
        
        record_query = db.query(models.Titre).filter(models.Titre.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Titre.name.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Titre, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Titre, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Titre, order_field).desc())

        total= record_query.count()

        record_query = record_query. offset((page - 1 ) * per_page). limit(per_page)

        return schemas.TitreResponseList(
            total= total,
            pages= math.ceil(total / per_page),
            per_page=per_page,
            current_page= page,
            data= record_query,

        )



titre = CRUDTitre(models.Titre) 