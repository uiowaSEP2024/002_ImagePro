"""create_jobs_table

Revision ID: abd2e54cef28
Revises: 19eb77a561bd
Create Date: 2023-03-22 20:57:24.877567

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "abd2e54cef28"
down_revision = "19eb77a561bd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("provider_id", sa.Integer(), nullable=False),
        sa.Column("provider_job_id", sa.String(), nullable=False),
        sa.Column("provider_job_name", sa.String(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_id", "provider_job_id"),
    )
    op.create_index(op.f("ix_jobs_customer_id"), "jobs", ["customer_id"], unique=False)
    op.create_index(op.f("ix_jobs_id"), "jobs", ["id"], unique=False)
    op.create_index(op.f("ix_jobs_provider_id"), "jobs", ["provider_id"], unique=False)
    op.create_index(
        op.f("ix_jobs_provider_job_id"), "jobs", ["provider_job_id"], unique=False
    )
    op.create_index(
        op.f("ix_jobs_provider_job_name"), "jobs", ["provider_job_name"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_jobs_provider_job_name"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_provider_job_id"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_provider_id"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_id"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_customer_id"), table_name="jobs")
    op.drop_table("jobs")
