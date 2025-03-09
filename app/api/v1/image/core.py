from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import ImageMetadata, PCAResult, KMeansSegmentation
from app.services.auth_service import auth_service
from app.tasks import process_5d_image_task, perform_pca_analysis
import shutil
import os
from app.core.config import settings

router = APIRouter()


class ImageHandler:
    def __init__(self, db: Session):
        self.db = db

    def save_file(self, file: UploadFile) -> str:
        file_path = os.path.join(settings.UPLOAD_FOLDER, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File save error: {str(e)}")

    def store_metadata(self, filename: str, file_path: str) -> ImageMetadata:
        metadata = ImageMetadata(filename=filename, width=0, height=0, channels=0, bands=0, file_path=file_path)
        self.db.add(metadata)
        self.db.commit()
        self.db.refresh(metadata)
        return metadata


@router.post("/image-upload/")
async def upload_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: str = Depends(auth_service.decode_token)
):
    handler = ImageHandler(db)
    file_path = handler.save_file(file)
    metadata = handler.store_metadata(file.filename, file_path)
    task = process_5d_image_task.delay(file_path)
    return {"image_id": metadata.id, "filename": file.filename, "task_id": task.id}


@router.get("/{image_id}/metadata/")
def get_image_metadata(image_id: int, db: Session = Depends(get_db)):
    metadata = db.query(ImageMetadata).filter(ImageMetadata.id == image_id).first()
    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")
    return metadata


@router.post("/{image_id}/pca/")
def perform_pca(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageMetadata).filter(ImageMetadata.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    task = perform_pca_analysis.delay(image.file_path)
    return {"image_id": image.id, "task_id": task.id}


@router.get("/{image_id}/result/")
def get_processed_results(image_id: int, db: Session = Depends(get_db)):
    pca_result = db.query(PCAResult).filter(PCAResult.image_id == image_id).first()
    kmeans_result = db.query(KMeansSegmentation).filter(KMeansSegmentation.image_id == image_id).first()
    if not (pca_result or kmeans_result):
        raise HTTPException(status_code=404, detail="No processing results found")
    return {"pca": pca_result, "kmeans": kmeans_result}
