import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_, and_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models, schemas
from datetime import datetime

class CRUDrendez_vous(CRUDBase[models.Rendez_Vous, schemas.Rendez_VousCreate, schemas.Rendez_VousUpdate]):

    @classmethod
    def get_by_uuid(cls, db: Session, uuid: str):
        return db.query(models.Rendez_Vous).filter(models.Rendez_Vous.uuid == uuid, models.Rendez_Vous.is_deleted == False).first()
    
    @classmethod
    def get_by_consultant_uuid(cls, db: Session, consultant_uuid: str):
        return db.query(models.Rendez_Vous).filter(models.Rendez_Vous.consultant_uuid == consultant_uuid, models.Rendez_Vous.is_deleted == False).all()

    @classmethod
    def get_by_patient_uuid(cls, db: Session, patient_uuid: str):
        return db.query(models.Rendez_Vous).filter(models.Rendez_Vous.patient_uuid == patient_uuid, models.Rendez_Vous.is_deleted == False).all()
    
    @classmethod
    def get_by_status(cls, db: Session, status: str):
        return db.query(models.Rendez_Vous).filter(models.Rendez_Vous.status == status, models.Rendez_Vous.is_deleted == False).first()

    @classmethod
    def delete(cls, db: Session, uuid: str):
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail="rendez-vous-not-found")
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls, db: Session, uuid: str):
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail="rendez-vous-not-found")
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def create(cls, db: Session, obj_in: schemas.Rendez_VousCreate):
        # Vérification chevauchement rendez-vous
        conflict = db.query(models.Rendez_Vous).filter(
            models.Rendez_Vous.consultant_uuid == obj_in.consultant_uuid,
            models.Rendez_Vous.date_rendez_vous == obj_in.date_rendez_vous,
            models.Rendez_Vous.is_deleted == False,
            or_(
                and_(models.Rendez_Vous.start_time <= obj_in.start_time, models.Rendez_Vous.end_time > obj_in.start_time),
                and_(models.Rendez_Vous.start_time < obj_in.end_time, models.Rendez_Vous.end_time >= obj_in.end_time),
                and_(models.Rendez_Vous.start_time >= obj_in.start_time, models.Rendez_Vous.end_time <= obj_in.end_time)
            )
        ).first()
        if conflict:
            raise HTTPException(status_code=400, detail="Ce consultant a déjà un rendez-vous pendant cette plage horaire.")

        db_obj = models.Rendez_Vous(
            uuid=str(uuid.uuid4()),
            consultant_uuid=obj_in.consultant_uuid,
            patient_uuid=obj_in.patient_uuid,
            date_rendez_vous=obj_in.date_rendez_vous,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @classmethod
    def update(cls, db: Session, obj_in: schemas.Rendez_VousUpdate, added_by: str):
        db_obj = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail="rendez-vous-not-found")

        # Vérification chevauchement pour update
        if obj_in.consultant_uuid or obj_in.start_time or obj_in.end_time or obj_in.date_rendez_vous:
            consultant_uuid = obj_in.consultant_uuid if obj_in.consultant_uuid else db_obj.consultant_uuid
            start_time = obj_in.start_time if obj_in.start_time else db_obj.start_time
            end_time = obj_in.end_time if obj_in.end_time else db_obj.end_time
            date_rendez_vous = obj_in.date_rendez_vous if obj_in.date_rendez_vous else db_obj.date_rendez_vous

            conflict = db.query(models.Rendez_Vous).filter(
                models.Rendez_Vous.consultant_uuid == consultant_uuid,
                models.Rendez_Vous.date_rendez_vous == date_rendez_vous,
                models.Rendez_Vous.uuid != db_obj.uuid,
                models.Rendez_Vous.is_deleted == False,
                or_(
                    and_(models.Rendez_Vous.start_time <= start_time, models.Rendez_Vous.end_time > start_time),
                    and_(models.Rendez_Vous.start_time < end_time, models.Rendez_Vous.end_time >= end_time),
                    and_(models.Rendez_Vous.start_time >= start_time, models.Rendez_Vous.end_time <= end_time)
                )
            ).first()
            if conflict:
                raise HTTPException(status_code=400, detail="Ce consultant a déjà un rendez-vous pendant cette plage horaire.")

        db_obj.consultant_uuid = obj_in.consultant_uuid if obj_in.consultant_uuid else db_obj.consultant_uuid
        db_obj.patient_uuid = obj_in.patient_uuid if obj_in.patient_uuid else db_obj.patient_uuid
        db_obj.date_rendez_vous = obj_in.date_rendez_vous if obj_in.date_rendez_vous else db_obj.date_rendez_vous
        db_obj.start_time = obj_in.start_time if obj_in.start_time else db_obj.start_time
        db_obj.end_time = obj_in.end_time if obj_in.end_time else db_obj.end_time
        db_obj.status = obj_in.status if obj_in.status else db_obj.status
        db_obj.added_by = added_by
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update_status(cls, db: Session, uuid: str, is_active: bool):
        db_obj = cls.get_by_uuid(db, uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="rendez-vous-not-found"))
        db_obj.is_active = is_active
        db.commit()

    @classmethod
    def get_many(
        cls,
        db: Session,
        page: int = 1,
        per_page: int = 25,
    ):
        record_query = db.query(models.Rendez_Vous).filter(models.Rendez_Vous.is_deleted == False)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)
        return schemas.Rendez_VousResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    


    @classmethod
    def get_consultant_rendez_vous(
        cls,
        db: Session,
        page: int = 1,
        per_page: int = 25,
        consultant_uuid: Optional[str]=None
    ):
        record_query = db.query=(models.Rendez_Vous).filter(models.Rendez_Vous.is_deleted == False,models.Rendez_Vous.consultant_uuid==consultant_uuid)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)
        return schemas.Rendez_VousResponseListSlim1(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )

rendez_vous = CRUDrendez_vous(models.Rendez_Vous)
