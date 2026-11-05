
from fastapi import FastAPI

from app.routes.colis import router as colis_router


app = FastAPI(
    title="Colis Service API",
    description="Microservice de gestion et de suivi des colis",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Bienvenue dans Colis Service",
        "service": "colis-service",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "service": "colis-service",
        "status": "healthy"
    }


# Register parcel routes
app.include_router(
    colis_router,
    prefix="/api/v1/colis",
    tags=["Colis"]
)
