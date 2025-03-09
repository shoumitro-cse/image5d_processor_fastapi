from fastapi import APIRouter
from app.api.v1 import image
from app.api.v1 import auth

router = APIRouter()


# for auth
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])


# for image
router.include_router(image.upload.router, prefix="/image", tags=["Image"])
router.include_router(image.metadata.router, prefix="/image", tags=["Image"])
router.include_router(image.slice.router, prefix="/image", tags=["Image"])
router.include_router(image.analyze.router, prefix="/image", tags=["Image"])
router.include_router(image.statistics.router, prefix="/image", tags=["Image"])
router.include_router(image.core.router, prefix="/image", tags=["Image"])