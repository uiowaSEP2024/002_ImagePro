"""create user hospital join table

Revision ID: f69b9a500cee
Revises: 7c316d7dd01f
Create Date: 2024-03-25 18:13:20.499715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f69b9a500cee"
down_revision = "7c316d7dd01f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_hospital",
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "hospital_id",
            sa.Integer(),
            sa.ForeignKey("hospitals.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade():
    op.drop_table("user_hospital")
