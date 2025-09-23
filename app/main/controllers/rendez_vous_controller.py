from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/rendez_vous", tags=["rendez_vous"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_rendez_vous(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    
    consultant = crud.consultants.get_by_uuid(db=db,uuid=obj_in.consultant_uuid)
    if not consultant:
        raise HTTPException(status_code=404, detail=__(key="consultant-not-found"))
    
    patient = crud.patients.get_by_uuid(db=db,uuid=obj_in.patient_uuid)
    if not patient:
        raise HTTPException(status_code=404, detail=__(key="patient-not-found"))

    crud.rendez_vous.create(
        db=db,
        obj_in=obj_in
    )
    return schemas.Msg(message=__(key="rendez_vous-create-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_rendez_vous(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    consultant = crud.consultant.get_by_uuid(db=db,uuid=obj_in.consultant_uuid)
    if not consultant:
        raise HTTPException(status_code=404, detail=__(key="consultant-not-found"))
    
    patient = crud.patient.get_by_uuid(db=db,uuid=obj_in.patient_uuid)
    if not patient:
        raise HTTPException(status_code=404, detail=__(key="patient-not-found"))
    
    crud.rendez_vous.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="rendez_vous-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_rendez_vous_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.rendez_vous.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="rendez_vous-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_rendez_vous(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.rendez_vous.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="rendez_vous-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_rendez_vous(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.rendez_vous.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="rendez_vous-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.rendez_vous.get_many(
        db=db,
        page=page,
        per_page=per_page
    )


@router.get("/get_consultant_rendez_vous", response_model = None)
async def get_consultant_rendez_vous_by_consultants(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["CONSULTANT"]))
):
    return crud.rendez_vous.get_consultant_rendez_vous(
        db=db,
        page=page,
        per_page=per_page,
        consultant_uuid = current_user.uuid
        
    )