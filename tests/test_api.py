import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_upload_image(mocker):
    """Test the image upload API with a mocked Celery task."""

    # Mock Celery task
    mock_task = mocker.patch("app.tasks.process_5d_image_task.delay")
    mock_task.return_value.id = "mock-task-id"

    # Use FastAPI's `app` inside the test
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/api/v1/image/upload/",
            files={"file": ("test.jpg", b"dummydata", "image/jpeg")},
        )

    assert response.status_code == 401
