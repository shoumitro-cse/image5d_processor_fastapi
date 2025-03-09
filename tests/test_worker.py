from app.celery_worker import celery_app


def test_worker_tasks():
    """Test that the Celery worker has registered tasks."""
    registered_tasks = celery_app.tasks.keys()
    assert "app.tasks.image_task.process_5d_image_task" in registered_tasks
