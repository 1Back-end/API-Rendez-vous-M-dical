from fastapi import APIRouter
from .migration_controller import router as migration
from .authentification_controller import router as authentication
from .user_controller import router as user
from .storage_controller import router as storage
from .address_controller import router as address
from .specialite_controller import router as specialite
from .sexe_controller import router as sexe
from .titres_controller import router as titre
from .hopital_controller import router as hospital
from .service_hopital_controller import router as service_hopitals
from .patient_controller import router as patient

api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(authentication)
api_router.include_router(user)
api_router.include_router(storage)
api_router.include_router(address)
api_router.include_router(specialite)
api_router.include_router(sexe)
api_router.include_router(titre)
api_router.include_router(hospital)
api_router.include_router(service_hopitals)
api_router.include_router(patient)