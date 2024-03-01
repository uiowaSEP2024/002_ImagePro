"""add study id to events

Revision ID: 12b9270616c1
Revises: 89bb3ebe71a7
Create Date: 2024-03-01 16:12:00.308920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "12b9270616c1"
down_revision = "89bb3ebe71a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "events",
        sa.Column("study_id", sa.Integer(), nullable=False, server_default="0"),
    )

    # Retrieve the events table
    events_table = sa.Table("events", sa.MetaData(), autoload_with=op.get_bind())

    # Update the study_id column with the value from job_id
    update_stmt = events_table.update().values(study_id=events_table.c.job_id)
    op.execute(update_stmt)

    op.create_index(op.f("ix_events_study_id"), "events", ["study_id"], unique=False)
    sa.ForeignKeyConstraint(
        ["study_id"],
        ["studies.id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # drop study id from events
    op.drop_index(op.f("ix_events_study_id"), table_name="events")
    op.drop_column("events", "study_id")
    # ### end Alembic commands ###
