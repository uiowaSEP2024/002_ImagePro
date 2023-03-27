"""Add columns first_name, last_name

Revision ID: 558baa280b8f
Revises: 19eb77a561bd
Create Date: 2023-03-20 14:57:07.905913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "558baa280b8f"
down_revision = "19eb77a561bd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column(
    #     "users",
    #     sa.Column("first_name", sa.String(), nullable=False),
    #     sa.Column("last_name", sa.String(), nullable=False),
    # )
    op.add_column("users", sa.Column("first_name", sa.String(), nullable=False))
    op.add_column("users", sa.Column("last_name", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", sa.Column("first_name"))
    op.drop_column("users", sa.Column("last_name"))
