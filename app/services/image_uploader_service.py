import shutil
import os
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.services.auth_service import auth_service
from app.services.image_service import ImageService
from app.tasks import process_5d_image_task
from fastapi import UploadFile, Depends, HTTPException


class Image5DUploaderService:
    """Class-based view for handling image upload and processing."""

    def __init__(self, db: Session, user: str):
        self.db = db
        self.user = user

    @staticmethod
    def save_file(file: UploadFile) -> str:
        """Saves the uploaded file to disk."""
        file_path = os.path.join(settings.UPLOAD_FOLDER, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File save error: {str(e)}")

    @staticmethod
    def process_image(file_path: str) -> str:
        """Triggers image processing via Celery."""

        if not os.path.exists(file_path):
            return "File not found"

        task = process_5d_image_task.delay(file_path)
        return task.id

    async def upload(self, file: UploadFile) -> dict:
        """Handles the entire image upload process."""
        file_path = self.save_file(file)
        task_id = self.process_image(file_path)
        return {"filename": file.filename, "task_id": task_id, "uploaded_by": self.user}

    @staticmethod
    def get_uploader(
        db: Session = Depends(get_db),
        current_user: str = Depends(auth_service.decode_token)
    ):
        """Creates and returns an Image5DUploaderService instance."""
        return Image5DUploaderService(db, current_user)


class ImageMetadataHandler:
    """Class to handle image metadata retrieval."""

    def __init__(self, filename: str):
        self.filename = filename
        self.file_path = os.path.join(settings.UPLOAD_FOLDER, filename)

    def validate_file(self):
        """Check if the file exists."""
        if not os.path.exists(self.file_path):
            raise HTTPException(status_code=404, detail="File not found")

    def get_metadata(self):
        """Extracts metadata from the image."""
        try:
            self.validate_file()
            image = ImageService.load_image(self.file_path)
            metadata = ImageService.get_image_metadata(image)

            # ✅ Convert NumPy data types to standard Python types
            for key, value in metadata.items():
                if hasattr(value, "item"):  # Handles NumPy scalars like np.uint8, np.int32
                    metadata[key] = value.item()

            return {"filename": self.filename, "metadata": metadata}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    @staticmethod
    def get_metadata_handler(filename: str):
        """Dependency injection to create an instance of ImageMetadataHandler."""
        return ImageMetadataHandler(filename)