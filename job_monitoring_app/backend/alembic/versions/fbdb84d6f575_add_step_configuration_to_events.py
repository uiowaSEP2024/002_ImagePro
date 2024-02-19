"""Add step_configuration to events

Revision ID: fbdb84d6f575
Revises: 25937391b16e
Create Date: 2023-04-29 20:09:34.613771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fbdb84d6f575"
down_revision = "25937391b16e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "events", sa.Column("step_configuration_id", sa.Integer(), nullable=True)
    )
    op.create_index(
        op.f("ix_events_step_configuration_id"),
        "events",
        ["step_configuration_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_events_step_configuration_id",
        "events",
        "step_configurations",
        ["step_configuration_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_events_step_configuration_id", "events", type_="foreignkey")
    op.drop_index(op.f("ix_events_step_configuration_id"), table_name="events")
    op.drop_column("events", "step_configuration_id")
