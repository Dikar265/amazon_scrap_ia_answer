"""Add vector column to products

Revision ID: d4466e25efee
Revises: 
Create Date: 2025-08-13 18:54:26.851028

"""
from typing import Sequence, Union
from pgvector.sqlalchemy import Vector
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd4466e25efee'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Solo agregar la columna vector
    op.add_column('products', sa.Column('vector', Vector(1536), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar la columna vector
    op.drop_column('products', 'vector')
