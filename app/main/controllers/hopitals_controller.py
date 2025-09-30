from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/hopitals", tags=["hopitals"])

@router.post('/create',response_model=schemas.Msg,status_code=201)
async def create_hopitals(
    *,
    db:Session = Depends(get_db),
    obj_in:schemas.HopitalsCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN,ADMIN,EDIMESTRE"]))
    
):
    exist_name = crud.hopitals.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409,detail="hopitals-already-exist")
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404,detail="address-not-found")
    crud.hopitals.create(
        db=db,
        obj_in=obj_in,
        added_by= current_user.uuid
    )
    return schemas.Msg(message=__(key="product-create-successfully"))

    
