import os

import httpx
from sqlalchemy.orm import Session

from app.models.statut import Statut
from app.schemas.statut import StatutCreate


# Check that the parcel exists by asking the Colis Service.
# Returns True (exists), False (not found) or None (service unreachable).
# If COLIS_SERVICE_URL is not set, the check is skipped.
def colis_exists(colis_id) -> bool | None:
    base_url = os.getenv("COLIS_SERVICE_URL")
    if not base_url:
        return True

    try:
        response = httpx.get(f"{base_url}/api/v1/colis/{colis_id}", timeout=3)
    except httpx.HTTPError:
        return None

    return response.status_code == 200


# Tell the Notification Service that the status changed.
# Best effort: a failure never blocks the status change.
# (URL and format to agree on with the Notification Service owner)
def notify_status_change(statut: Statut) -> None:
    base_url = os.getenv("NOTIFICATION_SERVICE_URL")
    if not base_url:
        return

    try:
        httpx.post(
            f"{base_url}/api/v1/notifications/",
            json={
                "colis_id": str(statut.colis_id),
                "type": statut.libelle,
                "message": f"Votre colis est : {statut.libelle}",
            },
            timeout=3,
        )
    except httpx.HTTPError:
        pass


# CREATE: Record a new status for a parcel
def create_statut(db: Session, data: StatutCreate) -> Statut:
    new_statut = Statut(**data.model_dump())

    db.add(new_statut)
    db.commit()
    db.refresh(new_statut)

    notify_status_change(new_statut)

    return new_statut


# READ: Latest status of a parcel (the displayed status)
def get_current_statut(db: Session, colis_id) -> Statut | None:
    return db.query(Statut).filter(
        Statut.colis_id == colis_id
    ).order_by(Statut.date_changement.desc()).first()


# READ: Full history of a parcel, oldest first
def get_history(db: Session, colis_id) -> list[Statut]:
    return db.query(Statut).filter(
        Statut.colis_id == colis_id
    ).order_by(Statut.date_changement.asc()).all()
