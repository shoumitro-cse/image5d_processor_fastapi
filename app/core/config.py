import os
from dotenv import load_dotenv

# Explicitly specify the path to .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, ".env")

# Load environment variables
load_dotenv(env_path)
# print("DATABASE_URL: ", os.getenv("DATABASE_URL"))


class Settings:
    PROJECT_NAME = "FastAPI Image Processor"
    DATABASE_URL = os.getenv("DATABASE_URL")
    UPLOAD_FOLDER = "data/uploads"
    PROCESSED_FOLDER = "data/processed"
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")


settings = Settings()
