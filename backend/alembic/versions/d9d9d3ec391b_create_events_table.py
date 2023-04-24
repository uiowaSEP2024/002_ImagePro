"""create_events_table

Revision ID: d9d9d3ec391b
Revises: abd2e54cef28
Create Date: 2023-03-22 22:26:57.769709

"""
from alembic import op
import sqlalchemy as sa

revision = "d9d9d3ec391b"
down_revision = "abd2e54cef28"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column(
            "kind",
            sa.Enum("step", "error", "info", "complete", name="event_kind"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["job_id"],
            ["jobs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_events_id"), "events", ["id"], unique=False)
    op.create_index(op.f("ix_events_job_id"), "events", ["job_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_events_job_id"), table_name="events")
    op.drop_index(op.f("ix_events_id"), table_name="events")
    op.drop_table("events")
    sa.Enum("step", "error", "info", "complete", name="event_kind").drop(
        op.get_bind(), checkfirst=False
    )
