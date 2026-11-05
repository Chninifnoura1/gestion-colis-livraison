
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.colis import (
    ColisCreate,
    ColisUpdate,
    ColisResponse,
)
from app.services import colis_service


router = APIRouter()


# CREATE: Create a new parcel
@router.post(
    "/",
    response_model=ColisResponse,
    status_code=status.HTTP_201_CREATED
)
def create_colis(
    colis_data: ColisCreate,
    db: Session = Depends(get_db)
):
    return colis_service.create_colis(db, colis_data)


# READ: Get all parcels
@router.get("/", response_model=list[ColisResponse])
def get_all_colis(db: Session = Depends(get_db)):
    return colis_service.get_all_colis(db)


# READ: Track a parcel (public endpoint)
@router.get("/suivi/{numero_suivi}")
def track_colis(
    numero_suivi: str,
    db: Session = Depends(get_db)
):
    colis = colis_service.get_colis_by_tracking(db, numero_suivi)

    if colis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun colis trouvé avec ce numéro de suivi."
        )

    return {
        "numero_suivi": colis.numero_suivi,
        "nom": colis.nom,
        "destination": colis.destination,
        "date_creation": colis.date_creation,
        "message": "Colis trouvé. Le statut sera fourni par le Statut Service."
    }


# READ: Get parcel details by ID
@router.get("/{colis_id}", response_model=ColisResponse)
def get_colis(
    colis_id: UUID,
    db: Session = Depends(get_db)
):
    colis = colis_service.get_colis_by_id(db, colis_id)

    if colis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colis introuvable."
        )

    return colis


# UPDATE: Update a parcel
@router.put("/{colis_id}", response_model=ColisResponse)
def update_colis(
    colis_id: UUID,
    colis_data: ColisUpdate,
    db: Session = Depends(get_db)
):
    colis = colis_service.get_colis_by_id(db, colis_id)

    if colis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colis introuvable."
        )

    if not colis_data.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucune information à modifier."
        )

    return colis_service.update_colis(db, colis, colis_data)


# DELETE: Delete a parcel
@router.delete("/{colis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_colis(
    colis_id: UUID,
    db: Session = Depends(get_db)
):
    colis = colis_service.get_colis_by_id(db, colis_id)

    if colis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colis introuvable."
        )

    colis_service.delete_colis(db, colis)
    return None
