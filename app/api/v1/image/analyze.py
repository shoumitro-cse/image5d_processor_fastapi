from fastapi import APIRouter, HTTPException
from app.services.image_service import ImageService
import os
from app.core.config import settings
from fastapi import Response

router = APIRouter()


@router.post("/analyze")
def run_pca(filename: str, n_components: int = 3):
    """
    Run PCA on the specified image file and return the shape of the transformed image.

    Args:
        filename (str): Name of the image file.
        n_components (int, optional): Number of principal components to retain. Default is 3.

    Returns:
        - Image as a byte stream (PNG format) containing the PCA components.
    """
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        image = ImageService.load_image(file_path)  # Load image
        # pca_result = ImageService.apply_algo(image, n_components)  # Apply Algorithm
        pca_result = ImageService.apply_pca(image, n_components)  # Apply PCA
        # pca_result = ImageService.apply_pca_v1(image, n_components)  # Apply PCA
        return Response(content=pca_result, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during PCA processing: {str(e)}")
