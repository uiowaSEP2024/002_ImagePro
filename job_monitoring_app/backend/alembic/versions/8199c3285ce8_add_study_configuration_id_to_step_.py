"""add study configuration id to step configuration

Revision ID: 8199c3285ce8
Revises: c344af227d6c
Create Date: 2024-03-05 11:20:13.634570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8199c3285ce8"
down_revision = "c344af227d6c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "step_configurations",
        sa.Column(
            "study_configuration_id", sa.Integer(), nullable=False, server_default="0"
        ),
    )

    # Retrieve the step_configurations table
    step_configurations_table = sa.Table(
        "step_configurations", sa.MetaData(), autoload_with=op.get_bind()
    )

    # Update the study_configuration_id column with the value from job_configuration_id
    update_stmt = step_configurations_table.update().values(
        study_configuration_id=step_configurations_table.c.job_configuration_id
    )
    op.execute(update_stmt)

    sa.ForeignKeyConstraint(
        ["study_configuration_id"],
        ["study_configurations.id"],
    )
    sa.UniqueConstraint("study_configuration_id", "tag")

    op.create_index(
        op.f("ix_step_configurations_study_configuration_id"),
        "step_configurations",
        ["study_configuration_id"],
        unique=False,
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # drop study configuration id from step_configurations
    op.drop_index(
        op.f("ix_step_configurations_study_configuration_id"),
        table_name="step_configurations",
    )
    op.drop_column("step_configurations", "study_configuration_id")
    # ### end Alembic commands ###
