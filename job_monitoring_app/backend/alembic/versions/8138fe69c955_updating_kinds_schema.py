"""Updating kinds schema

Revision ID: 8138fe69c955
Revises: 8c4f7aee9b55
Create Date: 2024-02-22 18:17:56.609327

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8138fe69c955"
down_revision = "8c4f7aee9b55"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Alter the existing enum type to use the new values
    op.alter_column(
        "events",
        "kind",
        existing_type=sa.Enum(
            "Info", "Error", "Pending", "Complete", "In progress", name="event_kind"
        ),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "events",
        "kind",
        existing_type=sa.Enum("step", "error", "info", "complete", name="event_kind"),
        nullable=False,
    )
    # ### end Alembic commands ###
