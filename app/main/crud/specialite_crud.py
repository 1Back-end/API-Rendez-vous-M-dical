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
<<<<<<< HEAD
from app.main import models,schemas

class CRUDSpecialites(CRUDBase[models.Specialites,schemas.SpecialitesCreate,schemas.SpecialitesUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Specialites).filter(models.Specialites.uuid==uuid,models.Specialites.is_deleted==False).first()
    

    @classmethod
    def get_by_name(cls,db:Session,name:str):
        return db.query(models.Specialites).filter(models.Specialites.name==name,models.Specialites.is_deleted==False).first()
    
    @classmethod
    def update_status(cls,db:Session,uuid:str,is_active:bool):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="specialites-not-found")
        db_obj.is_active = is_active
        db.commit()
    
    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)  
        if not db_obj:
             raise HTTPException(status_code=404,detail=__(key="specialites-not-found"))
        db.delete(db_obj)
        db.commit()


    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="specialites-not-found")
        db_obj.is_deleted=True
        db.commit()


    @classmethod
    def create(cls,db:Session, obj_in:schemas.SpecialitesCreate,added_by:str):
        db_obj = models.Specialites(
            uuid = str(uuid.uuid4()),
            name = obj_in.name,
            added_by = added_by
=======
from app.main import models, schemas


class CRUDSpecialite(CRUDBase[models.Specialites, schemas.Specialites.Create, schemas.SpecialitesUpdate]):  # type: ignore

    @classmethod
    def get_by_uuid(cls, db: Session, uuid: str):
        return db.query(models.Specialites).filter(models.Specialites.uuid == uuid, models.Specialites.is_deleted == False).first()

    @classmethod
    def get_by_name(cls, db: Session, name: str):
        return db.query(models.Specialites).filter(models.Specialites.name == name, models.Specialites.is_deleted == False).first()

    @classmethod
    def delete(cls, db: Session, uuid: str):

        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(
                status_code=404, detail="speciality--not-found")
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls, db: Session, uuid: str):
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(
                status_code=404, detail="speciality-not-found")
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def create(cls, db: Session, obj_in: schemas.SpecialitesCreate, added_by: str):
        db_obj = models.Specialites(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            added_by=added_by
>>>>>>> 79ec58cd0c1a2119c875d4d68ce9c032b285010a
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    

    @classmethod
    def update(cls,db:Session,obj_in:schemas.SpecialitesUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid) 
        if not db_obj:
            raise HTTPException(status_code=404,detail="Specialites-not-found")
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
        
        record_query = db.query(models.Specialites).filter(models.Specialites.is_deleted == False)
=======
        keyword: Optional[str] = None,
    ):
        record_query = db.query(models.Specialites).filter(
            models.Specialites.is_deleted == False)
>>>>>>> 79ec58cd0c1a2119c875d4d68ce9c032b285010a

        if keyword:
            record_query = record_query.filter(
                or_(
<<<<<<< HEAD
                    models.Specialites.name.ilike(f'%{keyword}%')
=======
                    models.Specialites.name.ilike(f'%{keyword}%'),
>>>>>>> 79ec58cd0c1a2119c875d4d68ce9c032b285010a
                )
            )

        if order and order_field and hasattr(models.Specialites, order_field):
            if order == "asc":
<<<<<<< HEAD
                record_query = record_query.order_by(getattr(models.Specialites, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Specialites, order_field).desc())

        total= record_query.count()

        record_query = record_query. offset((page - 1 ) * per_page). limit(per_page)

        return schemas.SpecialitesResponseList(
            total= total,
            pages= math.ceil(total / per_page),
            per_page=per_page,
            current_page= page,
            data= record_query,

        )


specialites = CRUDSpecialites(models.Specialites) 
=======
                record_query = record_query.order_by(
                    getattr(models.Specialites, order_field).asc())
            else:
                record_query = record_query.order_by(
                    getattr(models.Specialites, order_field).desc())

        total = record_query.count()
        # Pagination avec offset et limit
        record_query = record_query.offset(
            (page - 1) * per_page).limit(per_page)

    @classmethod
    def update(cls, db: Session, obj_in: schemas.SpecialitesUpdate, added_by: str):
        db_obj = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(
                status_code=404, detail="speciality-not-found")
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.added_by = added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj


specialite = CRUDSpecialite(models.Specialites)
>>>>>>> 79ec58cd0c1a2119c875d4d68ce9c032b285010a
