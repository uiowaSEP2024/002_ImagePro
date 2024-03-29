"""Add users created_at and updated_at

Revision ID: 93033829c28e
Revises: 59d69860fd42
Create Date: 2023-04-25 11:44:20.243499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "93033829c28e"
down_revision = "59d69860fd42"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "users", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
