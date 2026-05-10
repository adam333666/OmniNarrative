from fastapi import APIRouter

from app.api.routes.config import router as config_router
from app.api.routes.creations import router as creations_router
from app.api.routes.internal import router as internal_router
from app.api.routes.system import router as system_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.api_prefix)
api_router.include_router(system_router)
api_router.include_router(config_router)
api_router.include_router(internal_router)
api_router.include_router(creations_router)
