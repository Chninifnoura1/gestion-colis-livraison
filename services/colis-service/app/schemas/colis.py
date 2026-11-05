
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Schema used when an agent creates a parcel
class ColisCreate(BaseModel):
    nom: str = Field(min_length=2, max_length=150)
    destination: str = Field(min_length=2, max_length=255)
    expediteur: str = Field(min_length=2, max_length=150)
    email_destinataire: EmailStr
    description: str | None = None


# Schema used when an agent updates a parcel
class ColisUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=2, max_length=150)
    destination: str | None = Field(default=None, min_length=2, max_length=255)
    expediteur: str | None = Field(default=None, min_length=2, max_length=150)
    email_destinataire: EmailStr | None = None
    description: str | None = None


# Schema returned by the API
class ColisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    numero_suivi: str
    nom: str
    destination: str
    expediteur: str
    email_destinataire: EmailStr
    description: str | None
    date_creation: datetime
