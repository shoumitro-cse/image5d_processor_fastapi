from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.v1.router_urls import router as v1_router


class FastAPIProcessorApp:
    def __init__(self):
        self.app = FastAPI(title="FastAPI Image Processor")
        self._register_routes()
        self._custom_openapi()

    def _register_routes(self):
        self.app.include_router(v1_router, prefix="/api/v1")

    def _custom_openapi(self):
        def custom_openapi():
            if self.app.openapi_schema:
                return self.app.openapi_schema
            openapi_schema = get_openapi(
                title="Your API",
                version="1.0.0",
                description="JWT Auth API with Bearer Token in Swagger UI",
                routes=self.app.routes,
            )
            openapi_schema["components"]["securitySchemes"] = {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
            for path in openapi_schema["paths"].values():
                for method in path.values():
                    method["security"] = [{"BearerAuth": []}]
            self.app.openapi_schema = openapi_schema
            return self.app.openapi_schema

        self.app.openapi = custom_openapi


api_processor_app = FastAPIProcessorApp()
app = api_processor_app.app
