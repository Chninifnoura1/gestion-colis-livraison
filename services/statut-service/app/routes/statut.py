from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.statut import StatutCreate, StatutResponse
from app.services import statut_service


router = APIRouter()


# CREATE: Record a status change (with the location)
@router.post(
    "/",
    response_model=StatutResponse,
    status_code=status.HTTP_201_CREATED
)
def create_statut(
    statut_data: StatutCreate,
    db: Session = Depends(get_db)
):
    exists = statut_service.colis_exists(statut_data.colis_id)

    if exists is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colis introuvable."
        )

    if exists is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Le service Colis est indisponible."
        )

    return statut_service.create_statut(db, statut_data)


# READ: Current status of a parcel
@router.get("/colis/{colis_id}/actuel", response_model=StatutResponse)
def get_current_statut(
    colis_id: UUID,
    db: Session = Depends(get_db)
):
    statut = statut_service.get_current_statut(db, colis_id)

    if statut is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun statut pour ce colis."
        )

    return statut


# READ: History of the steps of a parcel
@router.get("/colis/{colis_id}/historique", response_model=list[StatutResponse])
def get_history(
    colis_id: UUID,
    db: Session = Depends(get_db)
):
    return statut_service.get_history(db, colis_id)
