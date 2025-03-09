import numpy as np
import tifffile as tiff
from fastapi import APIRouter
import os
from app.core.config import settings
from app.services.image_service import ImageService

router = APIRouter()


@router.get("/statistics")
def get_image_statistics(filename: str):
    """
    API endpoint to return image statistics.
    """
    file_path = os.path.join(settings.UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # Load the image
    image = tiff.imread(file_path)

    # Compute statistics
    stats = ImageService.compute_statistics(image)
    histogram = ImageService.compute_histogram(image)
    band_stats = ImageService.get_statistics(image)

    return {
        "statistics": stats,
        "histogram": histogram,
        "band_statistic": band_stats,
        "band_statistic_size": len(band_stats),
    }
