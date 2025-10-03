from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/sexe", tags=["sexe"])


@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_patient(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.PatientCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_patient_email = crud.patient.get_by_email(db=db,email=obj_in.email)
    if exist_patient_email:
        raise HTTPException(status_code=409,detail=__(key="email-patient-already-exist"))
    
    exist_patient_phone_number = crud.patient.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_patient_phone_number:
         raise HTTPException(status_code=409,detail=__(key="phone-number-patient-already-exist"))
    
    if obj_in.phone_number_2:
        exist_patient_phone_number_2 = crud.patient.get_by_phone_number2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_patient_phone_number_2:
            raise HTTPException(status_code=409,detail=__(key="phone-number-2-patient-already-exist"))
        
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404,detail=__(key="address-not-found"))
    
    sexe = crud.sexe.get_by_uuid(db=db,uuid=obj_in.sexe_uuid)
    if not sexe:
        raise HTTPException(status_code=404,detail=__(key="sexe-not-found"))
    
    religion = crud.religion.get_by_uuid(db=db,uuid=obj_in.religion_uuid)
    if not religion:
        raise HTTPException(status_code=404,detail=__(key="religion-not-found"))

        
    crud.patient.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="patient-created-successfully"))



@router.put("/update",response_model=schemas.Msg,status_code=201)
async def update_patient(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.PatientUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_patient_email = crud.patient.get_by_email(db=db,email=obj_in.email)
    if exist_patient_email:
        raise HTTPException(status_code=409,detail=__(key="email-patient-already-exist"))
    
    exist_patient_phone_number = crud.patient.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_patient_phone_number:
        raise HTTPException(status_code=409,detail=__(key="phone-number-patient-already-exist"))
    
    if obj_in.phone_number_2:
        exist_patient_phone_number_2 = crud.patient.get_by_phone_number2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_patient_phone_number_2:
            raise HTTPException(status_code=409,detail=__(key="phone-number-2-patient-already-exist"))
        
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404,detail=__(key="address-not-found"))
    
    sexe = crud.sexe.get_by_uuid(db=db,uuid=obj_in.sexe_uuid)
    if not sexe:
        raise HTTPException(status_code=404,detail=__(key="sexe-not-found"))
    
    religion = crud.religion.get_by_uuid(db=db,uuid=obj_in.religion_uuid)
    if not religion:
        raise HTTPException(status_code=404,detail=__(key="religion-not-found"))
        
    crud.patient.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="patient-updated-successfully"))



@router.delete('/delete',response_model=schemas.Msg,status_code=200)
async def delete_patient(
     *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.patient.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="patient-deleted-successfully"))

@router.put('/soft_delete',response_model=schemas.Msg,status_code=200)
async def soft_delete_patient(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.patient.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="patient-deleted-successfully"))


@router.get('/get_by_uuid',response_model=schemas.PatientResponse,status_code=200)
async def get_patient_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    obj_in = crud.patient.get_by_uuid(db=db,uuid=uuid)
    if not obj_in:
        raise HTTPException(status_code=404,detail=__(key="user-not-found"))
    return obj_in


@router.get("/get_many", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 25,
    order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.patient.get_many(
        db, 
        page, 
        per_page,
        order,
        keyword,
        order_field
    )


@router.put("/update_status",response_model=schemas.Msg)
def update_status_patient(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.patient.update_status(
        db=db,
        uuid = obj_in.uuid,
        is_active = obj_in.is_active
    )
    return schemas.Msg(message=__(key="patient-update-status-successfully"))
