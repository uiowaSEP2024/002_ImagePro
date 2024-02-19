"""add_columns_first_name_last_name

Revision ID: b32b411f19a2
Revises: d9d9d3ec391b
Create Date: 2023-03-26 23:45:04.539777

"""
from alembic import op
import sqlalchemy as sa


revision = "b32b411f19a2"
down_revision = "d9d9d3ec391b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("first_name", sa.String(), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
