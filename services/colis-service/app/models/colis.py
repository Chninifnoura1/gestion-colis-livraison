
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Colis(Base):
    __tablename__ = "colis"
    __table_args__ = {"schema": "colis"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    numero_suivi: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    nom: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    destination: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    expediteur: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email_destinataire: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    date_creation: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
