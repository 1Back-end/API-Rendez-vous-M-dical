from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/titre", tags=["titre"])

@router.post("/create",response_model=schemas.Msg,status_code=201)
async def create_titre(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TitreCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    exist_name  = crud.titre.get_by_name(db=db,name=obj_in.name)
    if  exist_name:
        raise HTTPException(status_code=409, detail=__(key="titre-already-exist"))
    
    crud.titre.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="titre-created-successfully"))


@router.put("/update",response_model=schemas.Msg,status_code=200)
async def update_titre(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TitreUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    exist_name  = crud.titre.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="titre-already-exist"))
    
    crud.titre.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="titre-update-successfully"))


@router.delete("/delete",response_model=schemas.Msg,status_code=200)
async def delete_titre(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TitreDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.titre.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="titre-deleted-successfully"))

@router.put("/soft_delete",response_model=schemas.Msg,status_code=200)
async def soft_delete_titre(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TitreDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
    
):
    crud.titre.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="titre-deleted-successfully"))

@router.put("/update_status",response_model=schemas.Msg)
async def update_titre_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TitreUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.titre.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="titre-update-successfully"))


@router.get("/get_many", response_model = None)
async def get(
    *,
    db: Session = Depends(get_db),
    page : int = 1,
    per_page : int = 25,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.titre.get_many(
        db=db,
        page=page,
        per_page=per_page
    )




@router.get("get_by_uuid",response_model=schemas.TitreResponse)
async def get_titre_by_uuid(
    *,
    uuid: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    db_obj = crud.titre.get_by_uuid(db=db,uuid=uuid)
    if not db_obj:
        raise HTTPException(status_code=404,detail=__(key="titre-not-found"))
    return db_obj

