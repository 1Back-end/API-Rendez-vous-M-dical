from fastapi import APIRouter
from .migration_controller import router as migration
from .authentification_controller import router as authentication
from .user_controller import router as user
from .storage_controller import router as storage
from .address_controller import router as address
from .specialite_controller import router as specialite
from .titres_controller import router as titres
from .religion_controller import router as religion
from .sexe_controller import router as sexe
from .hopitals_controller import router as hopitals
from .service_hopitals_controller import router as service_hopitals
from .consultants_controller import router as consultants
from .rendez_vous_controller import router as rendez_vous
from .patients_controller import router as patients

api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(authentication)
api_router.include_router(user)
api_router.include_router(storage)
api_router.include_router(address)
api_router.include_router(specialite)
api_router.include_router(titres)
api_router.include_router(religion)
api_router.include_router(sexe)
api_router.include_router(hopitals)
api_router.include_router(service_hopitals)
api_router.include_router(consultants)
api_router.include_router(rendez_vous)
api_router.include_router(patients)
