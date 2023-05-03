"""Create job configurations table

Revision ID: affc3e689080
Revises: 6e69f4231372
Create Date: 2023-04-29 14:07:57.050469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "affc3e689080"
down_revision = "6e69f4231372"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "job_configurations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tag", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("provider_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_id", "tag", "version"),
    )
    op.create_index(
        op.f("ix_job_configurations_id"), "job_configurations", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_job_configurations_provider_id"),
        "job_configurations",
        ["provider_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_job_configurations_tag"), "job_configurations", ["tag"], unique=False
    )
    op.create_index(
        op.f("ix_job_configurations_version"),
        "job_configurations",
        ["version"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_job_configurations_version"), table_name="job_configurations"
    )
    op.drop_index(op.f("ix_job_configurations_tag"), table_name="job_configurations")
    op.drop_index(
        op.f("ix_job_configurations_provider_id"), table_name="job_configurations"
    )
    op.drop_index(op.f("ix_job_configurations_id"), table_name="job_configurations")
    op.drop_table("job_configurations")
    # ### end Alembic commands ###
