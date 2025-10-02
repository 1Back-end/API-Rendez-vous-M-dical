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
async def create_rendez_vous(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.Rendez_VousCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_Rendez_Vous = crud.rendez_Vous.get_by_name(db=db,name=obj_in.name)
    if exist_Rendez_Vous:
        raise HTTPException(status_code=409,detail=__(key="rendez_Vous-already-exist"))
    
    crud.rendez_Vous.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="rendez_Vous-created-successfully"))



@router.put("/update",response_model=schemas.Msg,status_code=201)
async def update_rendez_Vous(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.Rendez_VousUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_rendez_Vous = crud.rendez_Vous.get_by_name(db=db,name=obj_in.name)
    if exist_rendez_Vous:
        raise HTTPException(status_code=409,detail=__(key="rendez_Vous-already-exist"))
    
    crud.rendez_Vous.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="rendez_Vous-updated-successfully"))



@router.delete('/delete',response_model=schemas.Msg,status_code=200)
async def delete_rendez_Vous(
     *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.rendez_Vous.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="rendez_Vous-deleted-successfully"))

@router.put('/soft_delete',response_model=schemas.Msg,status_code=200)
async def soft_delete_rendez_Vous(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.rendez_Vous.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="rendez_Vous-deleted-successfully"))


@router.get('/get_by_uuid',response_model=schemas.Rendez_VousResponse,status_code=200)
async def get_rendez_Vous_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    obj_in = crud.rendez_Vous.get_by_uuid(db=db,uuid=uuid)
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
    return crud.rendez_Vous.get_many(
        db, 
        page, 
        per_page,
        order,
        keyword,
        order_field
    )


@router.put("/update_status",response_model=schemas.Msg)
def update_status_rendez_Vous(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.Rendez_VousUpdateStatus,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.rendez_Vous.update_status(
        db=db,
        uuid = obj_in.uuid,
        is_active = obj_in.is_active
    )
    return schemas.Msg(message=__(key="rendez_Vous-update-status-successfully"))
