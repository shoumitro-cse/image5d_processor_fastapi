import pytest
from app.tasks import process_5d_image_task


def test_process_image():
    """Test that the process_image task executes correctly."""
    file_path = "/Users/roy-mac/Desktop/image_processor/data/processed/mitosis-5d.tif"
    result = process_5d_image_task(file_path)
    assert result == f"Processed {file_path}"
