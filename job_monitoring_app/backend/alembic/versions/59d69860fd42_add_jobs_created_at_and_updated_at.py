"""Add jobs created_at and updated_at

Revision ID: 59d69860fd42
Revises: 5331874bbc80
Create Date: 2023-04-25 11:42:07.535710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59d69860fd42"
down_revision = "5331874bbc80"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "jobs",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "jobs", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("jobs", "updated_at")
    op.drop_column("jobs", "created_at")
