from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from app.services.image_service import ImageService
from app.core.config import settings
import os
from app.services.image_uploader_service import ImageMetadataHandler


router = APIRouter()


@router.get("/metadata")
def get_image_metadata(handler: ImageMetadataHandler = Depends(ImageMetadataHandler.get_metadata_handler)):
    """FastAPI route that retrieves image metadata using class-based logic."""
    return jsonable_encoder(handler.get_metadata())
