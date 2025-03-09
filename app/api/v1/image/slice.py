from fastapi import APIRouter
from app.services.image_service import ImageService
import os
from app.core.config import settings


router = APIRouter()


@router.get("/slice")
def get_slice(filename: str, t: int = 0, z: int = 0, c: int = 0):
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    try:
        image = ImageService.load_image(file_path)
        extracted_slice = ImageService.extract_slice(image, t, z, c)
        return {"slice_data": extracted_slice.tolist()}
    except Exception as e:
        return {"error": str(e)}

