"""remove job configuration from study

Revision ID: 9d6576f33144
Revises: ed38666cb87d
Create Date: 2024-03-06 23:27:45.252175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9d6576f33144"
down_revision = "23375153341b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_studies_job_configuration_id", table_name="studies")
    op.drop_column("studies", "job_configuration_id")


def downgrade() -> None:
    op.add_column(
        "studies",
        sa.Column(
            "job_configuration_id",
            sa.INTEGER(),
            nullable=True,
        ),
    )

    # Retrieve the studies table
    studies_table = sa.Table("studies", sa.MetaData(), autoload_with=op.get_bind())

    # Update the job_configuration_id column with the value from study_configuration_id
    update_stmt = studies_table.update().values(
        job_configuration_id=studies_table.c.study_configuration_id
    )
    op.execute(update_stmt)

    op.create_foreign_key(
        "fk_studies_job_configuration_id",
        "studies",
        "job_configurations",
        ["job_configuration_id"],
        ["id"],
    )
    op.create_index(
        "ix_studies_job_configuration_id",
        "studies",
        ["job_configuration_id"],
        unique=False,
    )
