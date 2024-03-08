"""remove job configuration from step configurations

Revision ID: b4a81b0429b4
Revises: 9d6576f33144
Create Date: 2024-03-06 23:34:50.629211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b4a81b0429b4"
down_revision = "9d6576f33144"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index(
        "ix_step_configurations_job_configuration_id", table_name="step_configurations"
    )
    op.drop_column("step_configurations", "job_configuration_id")


def downgrade() -> None:
    op.add_column(
        "step_configurations",
        sa.Column(
            "job_configuration_id", sa.INTEGER(), nullable=False, server_default="0"
        ),
    )

    # Retrieve the step_configurations table
    step_configurations_table = sa.Table(
        "step_configurations", sa.MetaData(), autoload_with=op.get_bind()
    )

    # Update the job_configuration_id column with the value from study_configuration_id
    update_stmt = step_configurations_table.update().values(
        job_configuration_id=step_configurations_table.c.study_configuration_id
    )
    op.execute(update_stmt)

    op.create_index(
        "ix_step_configurations_job_configuration_id",
        "step_configurations",
        ["job_configuration_id"],
        unique=False,
    )
