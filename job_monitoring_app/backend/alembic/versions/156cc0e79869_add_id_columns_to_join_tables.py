"""add id columns to join tables

Revision ID: 156cc0e79869
Revises: c4ad4636595f
Create Date: 2024-04-03 16:04:51.572489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "156cc0e79869"
down_revision = "c4ad4636595f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user_provider",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            primary_key=True,
            autoincrement=True,
            server_default=sa.text("nextval('user_provider_id_seq'::regclass)"),
        ),
    )

    op.add_column(
        "user_hospital",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            primary_key=True,
            autoincrement=True,
            server_default=sa.text("nextval('user_hospital_id_seq'::regclass)"),
        ),
    )


def downgrade() -> None:
    op.drop_column("user_provider", "id")
    op.drop_column("user_hospital", "id")
