"""Heroes table init

Revision ID: e5e10986fe96
Revises:
Create Date: 2025-07-14 14:43:39.728353

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5e10986fe96"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "heroes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("intelligence", sa.Integer(), nullable=True),
        sa.Column("strength", sa.Integer(), nullable=True),
        sa.Column("speed", sa.Integer(), nullable=True),
        sa.Column("power", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_heroes")),
        sa.UniqueConstraint("name", name=op.f("uq_heroes_name")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("heroes")
    # ### end Alembic commands ###
