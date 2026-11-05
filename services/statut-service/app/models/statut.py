import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Statut(Base):
    __tablename__ = "statut"
    __table_args__ = {"schema": "statut"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Id of the parcel (owned by the Colis Service)
    colis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    libelle: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    localisation: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    commentaire: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    date_changement: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
