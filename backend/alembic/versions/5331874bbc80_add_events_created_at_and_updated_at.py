"""Add events created_at and updated_at

Revision ID: 5331874bbc80
Revises: 6e1488440746
Create Date: 2023-04-25 11:40:43.721642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5331874bbc80"
down_revision = "6e1488440746"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "events", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("events", "updated_at")
    op.drop_column("events", "created_at")
