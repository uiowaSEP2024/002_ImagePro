"""Add api_keys created_at and updated_at

Revision ID: b6bcaa15f3ed
Revises: 93033829c28e
Create Date: 2023-04-25 11:44:57.750319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6bcaa15f3ed"
down_revision = "93033829c28e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "api_keys",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "api_keys", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("api_keys", "updated_at")
    op.drop_column("api_keys", "created_at")
