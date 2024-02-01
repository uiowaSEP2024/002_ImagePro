"""Add ApiKeys expires_at column

Revision ID: 8c4f7aee9b55
Revises: 744a41e3a995
Create Date: 2023-05-02 16:05:16.824332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8c4f7aee9b55"
down_revision = "744a41e3a995"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "api_keys", sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("api_keys", "expires_at")
