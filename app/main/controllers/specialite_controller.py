from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/specialite", tags=["specialite"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_specialite(
    *,
    db: Session = Depends(get_db),
    db_obj:schemas.SpecialiteCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    exist_name  = crud.specialite.get_by_name(db=db,name=db_obj.name)
    if  exist_name:
        raise HTTPException(status_code=409, detail=__(key="specialite-already-exist"))
    
    crud.specialite.create(
        db=db,
        db_obj=db_obj,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="specialite-created-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_specialite(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SpecialiteUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    exist_name  = crud.specialite.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="specialite-already-exist"))
    
    crud.specialite.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="specialite-update-successfully"))


@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_specialite(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SpecialiteDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.specialite.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="specialite-deleted-successfully"))

@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_specialite(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SpecialiteDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.specialite.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="user-deleted-successfully"))

@router.put("/update_status",response_model=schemas.Msg)
async def update_specialite_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.SpecialiteUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.specialite.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="specialite-update-successfully"))


@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.specialite.get_many(
        db=db,
        page=page,
        per_page=per_page
    )