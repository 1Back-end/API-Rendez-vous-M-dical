from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/Consultant", tags=["Consultant"])


@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_patient(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.ConsultantCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_consultant_first_name = crud.consulant.get_by_consultant(db=db,first_name=obj_in.first_name)
    if exist_consultant_first_name:
        raise HTTPException(status_code=409,detail=__(key="first_name-patient-already-exist"))
    
    exist_consultant_last_name = crud.consulant.get_by_consultant(db=db,last_name=obj_in.last_name)
    if exist_consultant_last_name:
        raise HTTPException(status_code=409,detail=__(key="last_name-patient-already-exist"))
    
    exist_consultant_phone_number = crud.consulant.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_consultant_phone_number:
         raise HTTPException(status_code=409,detail=__(key="phone-number-patient-already-exist"))
    
    if obj_in.phone_number_2:
        exist_consultant_phone_number_2 = crud.consulant.get_by_phone_number2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_consultant_phone_number_2:
            raise HTTPException(status_code=409,detail=__(key="phone-number-2-patient-already-exist"))
        
    
    if obj_in.email:
        exist_consultant_email = crud.consulant.get_by_email(db=db,email=obj_in.email)
        if exist_consultant_email:
            raise HTTPException(status_code=409,detail=__(key="email-patient-already-exist"))
        
    if obj_in.titre_uuid:
        exist_consultant_titre_uuid = crud.consulant.get_by_titre_uuid(db=db,titre_uuid=obj_in.titre_uuid)
        if exist_consultant_titre_uuid:
            raise HTTPException(status_code=409,detail=__(key="phone-number-2-patient-already-exist"))
        
    if obj_in.service_hopital_uuid:
        exist_consultant_service_hopital_uuid = crud.consulant.get_by_service_hopital_uuid(db=db,service_hopital_uuid=obj_in.service_hopital_uuid)
        if exist_consultant_service_hopital_uuid:
            raise HTTPException(status_code=409,detail=__(key="service-hopital-patient-already-exist"))
        
    if obj_in.specialite_uuid:
        exist_consultant_specialite_uuid = crud.consulant.get_by_specialite_uuid(db=db,specialite_uuid=obj_in.specialite_uuid)
        if exist_consultant_specialite_uuid:
            raise HTTPException(status_code=409,detail=__(key="specialite-patient-already-exist"))

        
    crud.consulant.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="consultant-created-successfully"))



@router.put("/update",response_model=schemas.Msg,status_code=201)
async def update_consultant(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.ConsultantUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
    
    
):
    exist_consultant_email = crud.consulant.get_by_email(db=db,email=obj_in.email)
    if exist_consultant_email:
        raise HTTPException(status_code=409,detail=__(key="email-consultant-already-exist"))
    
    exist_consultant_first_name = crud.consulant.get_by_first_name(db=db,first_name=obj_in.first_name)
    if exist_consultant_first_name:
        raise HTTPException(status_code=409,detail=__(key="first-name-consultant-already-exist"))
    
    exist_consultant_last_name = crud.consulant.get_by_last_name(db=db,last_name=obj_in.last_name)
    if exist_consultant_last_name:
        raise HTTPException(status_code=409,detail=__(key="last-name-consultant-already-exist"))
    
    
    
    exist_consultant_phone_number = crud.consulant.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_consultant_phone_number:
         raise HTTPException(status_code=409,detail=__(key="phone-number-patient-already-exist"))
    
    
    if obj_in.phone_number_2:
        exist_patient_phone_number_2 = crud.patient.get_by_phone_number2(db=db,phone_number_2=obj_in.phone_number_2)
        if exist_patient_phone_number_2:
            raise HTTPException(status_code=409,detail=__(key="phone-number-2-patient-already-exist"))
        
    exist_consultant_titre_uuid = crud.consulant.get_by_titre_uuid(db=db,titre_uuid=obj_in.titre_uuid)
    if exist_consultant_titre_uuid:
        raise HTTPException(status_code=409,detail=__(key="titre-uuid-consultant-already-exist"))
    
    exist_consultant_service_hopital_uuid = crud.consulant.get_by_service_hopital_uuid(db=db,service_hopital_uuid=obj_in.service_hopital_uuid)
    if exist_consultant_service_hopital_uuid:
        raise HTTPException(status_code=409,detail=__(key="service-hopital-consultant-already-exist"))
    
    exist_consultant_specialite_uuid = crud.consulant.get_by_specialite_uuid(db=db,specialite_uuid=obj_in.specialite_uuid)
    if exist_consultant_specialite_uuid:
        raise HTTPException(status_code=409,detail=__(key="specialite-consultant-already-exist"))
    
    
    crud.consulant.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="consultant-updated-successfully"))



@router.delete('/delete',response_model=schemas.Msg,status_code=200)
async def delete_consultant(
     *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.consulant.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="consultant-deleted-successfully"))

@router.put('/soft_delete',response_model=schemas.Msg,status_code=200)
async def soft_delete_consultant(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.consulant.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="consltant-deleted-successfully"))


@router.get('/get_by_uuid',response_model=schemas.ConsultantResponse,status_code=200)
async def get_consultant_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    obj_in = crud.consulant.get_by_uuid(db=db,uuid=uuid)
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
    return crud.consulant.get_many(
        db, 
        page, 
        per_page,
        order,
        keyword,
        order_field
    )


@router.put("/update_status",response_model=schemas.Msg)
def update_status_consultant(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ConsultantUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.consulant.update_status(
        db=db,
        uuid = obj_in.uuid,
        is_active = obj_in.is_active
    )
    return schemas.Msg(message=__(key="consultant-update-status-successfully"))
