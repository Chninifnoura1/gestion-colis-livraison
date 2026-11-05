
import secrets
from sqlalchemy.orm import Session

from app.models.colis import Colis
from app.schemas.colis import ColisCreate, ColisUpdate


# Generate a unique tracking number
def generate_tracking_number(db: Session) -> str:
    while True:
        numero = f"COL-{secrets.token_hex(5).upper()}"

        existing = db.query(Colis).filter(
            Colis.numero_suivi == numero
        ).first()

        if not existing:
            return numero


# CREATE: Create a new parcel
def create_colis(db: Session, colis_data: ColisCreate) -> Colis:
    numero = generate_tracking_number(db)

    new_colis = Colis(
        numero_suivi=numero,
        **colis_data.model_dump()
    )

    db.add(new_colis)
    db.commit()
    db.refresh(new_colis)

    return new_colis


# READ: Get all parcels
def get_all_colis(db: Session) -> list[Colis]:
    return db.query(Colis).order_by(
        Colis.date_creation.desc()
    ).all()


# READ: Get a parcel by ID
def get_colis_by_id(db: Session, colis_id) -> Colis | None:
    return db.query(Colis).filter(
        Colis.id == colis_id
    ).first()


# READ: Find a parcel using its tracking number
def get_colis_by_tracking(db: Session, numero_suivi: str) -> Colis | None:
    return db.query(Colis).filter(
        Colis.numero_suivi == numero_suivi
    ).first()


# UPDATE: Update parcel information
def update_colis(
    db: Session,
    colis: Colis,
    colis_data: ColisUpdate
) -> Colis:
    update_data = colis_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(colis, field, value)

    db.commit()
    db.refresh(colis)

    return colis


# DELETE: Delete a parcel
def delete_colis(db: Session, colis: Colis) -> None:
    db.delete(colis)
    db.commit()
