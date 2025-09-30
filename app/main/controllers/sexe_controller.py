from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/sexe", tags=["sexe"])


@router.post("/create",response_model=schemas.Msg)
async def create_sexe(
        *,
        db: Session = Depends(get_db),
        obj_in : schemas.SexeCreate,
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.sexe.create(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="sexe-created-successfully"))

@router.put("/update",response_model=schemas.Msg)
async def update_sexe(
        *,
        db: Session = Depends(get_db),
        obj_in : schemas.SexeUpdate,
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.sexe.update(
        db=db,
        obj_in=obj_in,
        added_by=current_user.uuid
    )
    return schemas.Msg(message=__(key="sexe-update-successfully"))

@router.delete("/delete",response_model=schemas.Msg)
async def delete_sexe(
        *,
        db: Session = Depends(get_db),
        obj_in : schemas.SexeDelete,
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.sexe.delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="sexe-delete-successfully"))


@router.put("/soft-delete",response_model=schemas.Msg)
async def soft_delete_sexe(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.SexeDelete,
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.sexe.soft_delete(
        db=db,
        uuid=obj_in.uuid
    )
    return schemas.Msg(message=__(key="sexe-delete-successfully"))


@router.put("/update-status",response_model=schemas.Msg)
async def update_sexe_status(
        *,
        db: Session = Depends(get_db),
        obj_in : schemas.UpdateStatus,
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.sexe.update_status(
        db=db,
        uuid=obj_in.uuid,
        is_active=obj_in.is_active
    )
    return schemas.Msg(message=__(key="sexe-update-successfully"))


@router.get("/get_many", response_model=None)
def get(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 25,
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.sexe.get_many(
        db,
        page,
        per_page,
    )