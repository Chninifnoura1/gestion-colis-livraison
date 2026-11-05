"""create statut table

Revision ID: b7c3d9e41a52
Revises: 
Create Date: 2026-11-05 20:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7c3d9e41a52'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('statut',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('colis_id', sa.UUID(), nullable=False),
    sa.Column('libelle', sa.String(length=50), nullable=False),
    sa.Column('localisation', sa.String(length=255), nullable=True),
    sa.Column('commentaire', sa.Text(), nullable=True),
    sa.Column('date_changement', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='statut'
    )
    op.create_index(op.f('ix_statut_statut_colis_id'), 'statut', ['colis_id'], unique=False, schema='statut')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_statut_statut_colis_id'), table_name='statut', schema='statut')
    op.drop_table('statut', schema='statut')
