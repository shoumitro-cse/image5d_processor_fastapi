from celery import shared_task
from app.celery_worker import celery_app
from app.services.image_storage_service import ImageStorageService
from app.services.image_service import ImageService
from app.core.database import get_db
from app.models import PCAResult, ImageMetadata
import os


# @shared_task
@shared_task
def process_5d_image_task(file_path: str):
    # Apply PCA, Algo, Data store
    res = ImageStorageService.store_image_metadata(file_path)
    return {"message": res}


@celery_app.task
def image_detection_task():
    print("---image_detection_task---")


@celery_app.task
def perform_pca_analysis(image_id: int):
    """Performs PCA analysis on an image asynchronously."""
    db = next(get_db())  # Get database session

    # Fetch image metadata from the database
    image = db.query(ImageMetadata).filter(ImageMetadata.id == image_id).first()
    if not image:
        return {"error": "Image not found"}

    # Perform PCA analysis
    file_path = image.file_path
    if not os.path.exists(file_path):
        return {"error": "File path does not exist"}

    image = ImageService.load_image(file_path)
    pca_image = ImageService.apply_pca_v1(image)

    # Save PCA result in the database
    pca_result = PCAResult(image_id=image.id, img_bytes=pca_image)
    db.add(pca_result)
    db.commit()

    return {"message": "PCA analysis completed", "image_id": image.id}
