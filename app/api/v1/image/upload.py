from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.services.image_uploader_service import Image5DUploaderService

router = APIRouter()


@router.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    uploader: Image5DUploaderService = Depends(Image5DUploaderService.get_uploader)
):
    """FastAPI route that uses the class-based image upload handler."""
    response_data = await uploader.upload(file)
    return response_data
