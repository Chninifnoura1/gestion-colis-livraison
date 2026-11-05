from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.statut import router as statut_router


app = FastAPI(
    title="Statut Service API",
    description="Microservice de gestion des statuts et de l'historique des colis",
    version="1.0.0"
)

# Allow the React frontend to call this service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Bienvenue dans Statut Service",
        "service": "statut-service",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "service": "statut-service",
        "status": "healthy"
    }


# Register status routes
app.include_router(
    statut_router,
    prefix="/api/v1/statuts",
    tags=["Statuts"]
)
