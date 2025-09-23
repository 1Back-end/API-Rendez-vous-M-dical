from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/patient", tags=["patient"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_Patient(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    exist_phone_number = crud.patients.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409, detail=__(key="phone-number-already-exist"))
    
    if obj_in.phone_number_2:
        exist_phone_number_2 = crud.patients.get_by_phone_number_2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_phone_number_2:
            raise HTTPException(status_code=409, detail=__(key="phone-number-2-already-exist"))
        
    exist_email = crud.patients.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="patient-already-exist"))
    
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail=__(key="address-not-found"))
    
    sexe = crud.sexe.get_by_uuid(db=db,uuid=obj_in.sexe_uuid)
    if not sexe:
        raise HTTPException(status_code=404, detail=__(key="sexe-not-found"))
    
    religion = crud.religion.get_by_uuid(db=db,uuid=obj_in.religion_uuid)
    if not religion:
        raise HTTPException(status_code=404,detail=__(key="religion-not-found"))

    crud.patients.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="patient-create-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_Patient(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    exist_phone_number = crud.patients.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409, detail=__(key="patient-already-exist"))
    
    if obj_in.phone_number_2:
        exist_phone_number_2 = crud.patients.get_by_phone_number_2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_phone_number_2:
            raise HTTPException(status_code=409, detail=__(key="phone-number-2-already-exist"))
        
    exist_email = crud.patients.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="patient-already-exist"))
    
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail=__(key="address-not-found"))
    
    sexe = crud.sexe.get_by_uuid(db=db,uuid=obj_in.sexe_uuid)
    if not sexe:
        raise HTTPException(status_code=404, detail=__(key="sexe-not-found"))
    
    religion = crud.religion.get_by_uuid(db=db,uuid=obj_in.religion_uuid)
    if not religion:
        raise HTTPException(status_code=404,detail=__(key="religion-not-found"))
    
    crud.patients.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="patient-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_Patient_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.patients.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="patient-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_Hopitals(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.patients.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="patient-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_Patient(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.PatientDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.patients.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="patient-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.patients.get_many(
        db=db,
        page=page,
        per_page=per_page
    )