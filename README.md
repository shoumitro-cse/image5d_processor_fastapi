# FastAPI Image Processing Microservice

A high-performance image processing microservice built with FastAPI, Celery, and PostgreSQL. This service allows users to upload images, retrieve metadata, and perform advanced image processing tasks asynchronously.

## Features
- 📷 **Upload and store images**
- 🏷 **Retrieve image metadata**
- 🔄 **Perform PCA-based image analysis**
- 🖥 **Asynchronous background tasks with Celery**
- 🔌 **Dockerized setup for easy deployment**
- 📡 **REST API with FastAPI & auto-generated OpenAPI docs**

## Installation

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Redis (for Celery task queue)
- PostgreSQL (for metadata storage)

### Clone the Repository
```sh
git clone https://github.com/shoumitro-cse/image5d_processor_fastapi.git
cd image5d_processor_fastapi 
```

### Set Up Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file in the root directory and configure:
```ini
DATABASE_URL=postgresql://user:password@localhost:5432/image_db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_BACKEND_URL=db+postgresql://user:password@localhost:5432/image_db
```

### Run Migrations
```sh
alembic upgrade head
```

### Run the FastAPI Server
```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Redis & Celery Worker
```sh
redis-server &
celery -A app.workers.worker worker --loglevel=info
```

### Run with Docker (Recommended)
```sh
docker-compose up --build
```

## API Documentation
The API provides the following endpoints:

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/v1/image/upload/` | Upload an image |
| `GET`  | `/api/v1/image/{image_id}/metadata/` | Retrieve image metadata |
| `POST` | `/api/v1/image/{image_id}/pca/` | Perform PCA analysis on an image |
| `GET`  | `/api/v1/image/{image_id}/result/` | Retrieve processing results |

#### Access API Docs:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Running Tests
Unit tests cover all major functionalities. Run tests using:
```sh
pytest tests/ --cov=app --cov-report=term-missing
```

## Example Usage (Python Requests)
```python
import requests

url = "http://localhost:8000/api/v1/image/upload/"
files = {"file": open("sample.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## Jupyter Notebook Usage
A sample Jupyter Notebook demonstrating API interactions is available in `notebooks/`:
```sh
jupyter notebook notebooks/image_analysis_notebook.ipynb
```

## Deployment
### Using Gunicorn & Uvicorn Workers
```sh
gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000 --workers 4
```

### Deploy with Docker Compose
```sh
docker-compose up --build -d
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Added feature"`)
4. Push to branch (`git push origin feature-name`)
5. Create a Pull Request

## License
This project is licensed under the MIT License. See `LICENSE` for details.

