from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/Hopitals", tags=["Hopitals"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_Hopitals(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.HopitalsCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail=__(key="address-not-found"))
    
    exist_name = crud.hopitals.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="hopitals-already-exist"))
    
    crud.hopitals.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="hopitals-create-successfully"))

    

@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_Hopitals(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.HopitalsUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail=__(key="address-not-found"))
    
    exist_name = crud.hopitals.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="hopitals-already-exist"))
    
    crud.hopitals.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="hopitals-update-successfully"))


@router.put("/update_status",response_model=schemas.Msg)
async def update_Hopitals_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.HopitalsUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.hopitals.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="hopitals-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_Hopitals(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.HopitalsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.hopitals.delete(
        db=db,
        uuid=obj_in.uuid
    )

    crud.hopitals.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="hopitals-deleted-successfully"))


@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_Hopitals(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.HopitalsDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.hopitals.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="hopitals-deleted-successfully"))

@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.hopitals.get_many(
        db=db,
        page=page,
        per_page=per_page
    )
