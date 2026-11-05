from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# The only statuses allowed (business rule 4.2)
StatutLibelle = Literal[
    "en préparation",
    "expédié",
    "en cours de livraison",
    "livré",
    "en retard",
]


# Schema used when an agent records a status change
class StatutCreate(BaseModel):
    colis_id: UUID
    libelle: StatutLibelle
    localisation: str | None = Field(default=None, max_length=255)
    commentaire: str | None = None


# Schema returned by the API
class StatutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    colis_id: UUID
    libelle: str
    localisation: str | None
    commentaire: str | None
    date_changement: datetime
