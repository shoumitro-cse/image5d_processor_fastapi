from celery import Celery
from app.core.config import settings


class CeleryConfig:
    def __init__(self):
        self.app = Celery(
            "img_celery_worker",
            broker=settings.CELERY_BROKER_URL,
            backend=settings.CELERY_BACKEND_URL
        )
        self.app.autodiscover_tasks(['app'])
        # self.configure()

    def configure(self):
        """Apply custom configurations to Celery."""
        self.app.conf.update(
            task_routes={
                "app.tasks.image_tasks.*": {"queue": "image_processing"}
            },
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
        )

    def get_celery_app(self):
        """Returns the configured Celery app instance."""
        return self.app


# Create a singleton instance
celery_instance = CeleryConfig()
celery_app = celery_instance.get_celery_app()
