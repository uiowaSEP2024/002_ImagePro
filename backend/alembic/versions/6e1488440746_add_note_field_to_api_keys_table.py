"""Add Note field to API Keys table

Revision ID: 6e1488440746
Revises: 97c85d02b221
Create Date: 2023-04-20 01:42:25.121528

"""
from alembic import op
import sqlalchemy as sa



revision = "6e1488440746"
down_revision = "97c85d02b221"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("api_keys", sa.Column("note", sa.String(), nullable=True))



def downgrade() -> None:
    op.drop_column("api_keys", "note")
