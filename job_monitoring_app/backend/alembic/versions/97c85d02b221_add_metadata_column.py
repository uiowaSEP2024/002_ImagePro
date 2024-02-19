"""add metadata_column

Revision ID: 97c85d02b221
Revises: b32b411f19a2
Create Date: 2023-04-15 22:48:49.447890

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "97c85d02b221"
down_revision = "b32b411f19a2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column(
            "event_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_column("events", "event_metadata")
