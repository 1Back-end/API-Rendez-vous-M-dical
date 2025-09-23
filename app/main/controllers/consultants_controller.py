from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/consultants", tags=["consultants"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_consultants(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantsCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    exist_phone_number = crud.consultants.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409, detail=__(key="phone-number-already-exist"))
    
    if obj_in.phone_number_2:
        exist_phone_number_2 = crud.consultants.get_by_phone_number_2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_phone_number_2:
            raise HTTPException(status_code=409, detail=__(key="phone-number-2-already-exist"))
        
    exist_email = crud.consultants.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="consultants-already-exist"))
    
    titre = crud.titre.get_by_uuid(db=db,uuid=obj_in.titre_uuid)
    if not titre:
        raise HTTPException(status_code=404, detail=__(key="titre-not-found"))
    
    service_hopital = crud.service_hopitals.get_by_uuid(db=db,uuid=obj_in.service_hopital_uuid)
    if not service_hopital:
        raise HTTPException(status_code=404, detail=__(key="service_hopital-not-found"))
    
    specialite = crud.specialite.get_by_uuid(db=db,uuid=obj_in.specialite_uuid)
    if not specialite:
        raise HTTPException(status_code=404,detail=__(key="specialite-not-found"))

    crud.consultants.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="consultants-create-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_consultants(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantsUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    exist_phone_number = crud.consultants.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409, detail=__(key="phone-number-already-exist"))
    
    if obj_in.phone_number_2:
        exist_phone_number_2 = crud.consultants.get_by_phone_number_2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_phone_number_2:
            raise HTTPException(status_code=409, detail=__(key="phone-number-2-already-exist"))
        
    exist_email = crud.consultants.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="patient-already-exist"))
    
    titre = crud.titre.get_by_uuid(db=db,uuid=obj_in.titre_uuid)
    if not titre:
        raise HTTPException(status_code=404, detail=__(key="titre-not-found"))
    
    service_hopital = crud.service_hopitals.get_by_uuid(db=db,uuid=obj_in.service_hopital_uuid)
    if not service_hopital:
        raise HTTPException(status_code=404, detail=__(key="service_hopital-not-found"))
    
    specialite = crud.specialite.get_by_uuid(db=db,uuid=obj_in.specialite_uuid)
    if not specialite:
        raise HTTPException(status_code=404,detail=__(key="specialite-not-found"))
    
    crud.consultants.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="consultants-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_consultants_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantsUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.consultants.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="consultants-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_Hopitals(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.consultants.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="consultants-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_consultants(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.consultants.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="consultants-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.consultants.get_many(
        db=db,
        page=page,
        per_page=per_page
    )