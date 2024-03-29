"""Add studies, relationship with users, job_config

Revision ID: 89bb3ebe71a7
Revises: f5e0f22bbaea
Create Date: 2024-03-01 15:47:40.098604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "89bb3ebe71a7"
down_revision = "f5e0f22bbaea"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # Create studies table
    op.create_table(
        "studies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("provider_id", sa.Integer(), nullable=False),
        sa.Column("provider_study_id", sa.String(), nullable=False),
        sa.Column("provider_study_name", sa.String(), nullable=True),
        sa.Column("hospital_id", sa.Integer(), nullable=False),
        sa.Column("job_configuration_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["hospital_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["job_configuration_id"], ["job_configurations.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_id", "provider_study_id"),
    )

    op.create_index(
        op.f("ix_studies_hospital_id"), "studies", ["hospital_id"], unique=False
    )
    op.create_index(op.f("ix_studies_id"), "studies", ["id"], unique=False)
    op.create_index(
        op.f("ix_studies_job_configuration_id"),
        "studies",
        ["job_configuration_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_studies_provider_id"), "studies", ["provider_id"], unique=False
    )
    op.create_index(
        op.f("ix_studies_provider_study_id"),
        "studies",
        ["provider_study_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_studies_provider_study_name"),
        "studies",
        ["provider_study_name"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Delete studies table
    op.drop_index(op.f("ix_studies_provider_study_name"), table_name="studies")
    op.drop_index(op.f("ix_studies_provider_study_id"), table_name="studies")
    op.drop_index(op.f("ix_studies_provider_id"), table_name="studies")
    op.drop_index(op.f("ix_studies_job_configuration_id"), table_name="studies")
    op.drop_index(op.f("ix_studies_id"), table_name="studies")
    op.drop_index(op.f("ix_studies_hospital_id"), table_name="studies")
    op.drop_table("studies")
    # ### end Alembic commands ###
