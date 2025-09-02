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


class CRUDHopitals(CRUDBase[models.Hopitals, schemas.HopitalsCreate, schemas.HopitalsUpdate]): # type: ignore

    @classmethod
    def get_by_uuid(cls, db: Session, uuid: str):
        return db.query(models.Hopitals).filter(models.Hopitals.uuid == uuid,models.Hopitals.is_deleted==False).first()

    @classmethod
    def get_by_name(cls, db: Session, name: str):
        return db.query(models.Hopitals).filter(models.Hopitals.name == name,models.Hopitals.is_deleted==False).first()

    @classmethod
    def delete(cls, db: Session, uuid: str):

        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(
                status_code=404, detail="hopitals-not-found")
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls, db: Session, uuid: str):
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(
                status_code=404, detail="hopitals-not-found")
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def create(cls, db: Session, obj_in: schemas.HopitalsCreate,added_by:str):
        db_obj = models.Hopitals(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            abbrevation=obj_in.abbreviation,
            address_uuid=obj_in.address_uuid,
            added_by = added_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update(cls, db: Session, obj_in: schemas.HopitalsUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(
                status_code=404, detail="hopital-not-found")
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.abbrevation = obj_in.abbrevation if obj_in.abbrevation else db_obj.abbrevation
        db_obj.address_uuid=obj_in.address_uuid if db_obj.address_uuid else db_obj.address_uuid
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
        record_query = db.query(models.Hopitals).filter( models.Hopitals.is_deleted == False)
        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Hopitals.name.ilike(f'%{keyword}%'),
                )
            )

        if order and order_field and hasattr(models.Hopitals, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Hopitals, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Hopitals, order_field).desc())

        total = record_query.count() 
        # Pagination avec offset et limit
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        # Retourne une réponse paginée avec total, pages, page actuelle, nombre par page et liste des données
        return schemas.HospitalsResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query,
        )


hopitals = CRUDHopitals(models.Hopitals)