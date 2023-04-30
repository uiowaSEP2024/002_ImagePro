"""Create step configurations table

Revision ID: 25937391b16e
Revises: 4852f79e6d5f
Create Date: 2023-04-29 19:04:03.652710

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "25937391b16e"
down_revision = "4852f79e6d5f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "step_configurations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tag", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("job_configuration_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["job_configuration_id"],
            ["job_configurations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_configuration_id", "tag"),
    )
    op.create_index(
        op.f("ix_step_configurations_id"), "step_configurations", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_step_configurations_job_configuration_id"),
        "step_configurations",
        ["job_configuration_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_step_configurations_name"),
        "step_configurations",
        ["name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_step_configurations_points"),
        "step_configurations",
        ["points"],
        unique=False,
    )
    op.create_index(
        op.f("ix_step_configurations_tag"), "step_configurations", ["tag"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_step_configurations_tag"), table_name="step_configurations")
    op.drop_index(
        op.f("ix_step_configurations_points"), table_name="step_configurations"
    )
    op.drop_index(op.f("ix_step_configurations_name"), table_name="step_configurations")
    op.drop_index(
        op.f("ix_step_configurations_job_configuration_id"),
        table_name="step_configurations",
    )
    op.drop_index(op.f("ix_step_configurations_id"), table_name="step_configurations")
    op.drop_table("step_configurations")
