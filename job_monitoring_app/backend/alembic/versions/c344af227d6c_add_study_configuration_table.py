"""add study configuration table

Revision ID: c344af227d6c
Revises: 593cd73ffb81
Create Date: 2024-03-05 11:06:20.355274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c344af227d6c"
down_revision = "593cd73ffb81"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "study_configurations",
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
        op.f("ix_study_configurations_id"), "study_configurations", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_study_configurations_provider_id"),
        "study_configurations",
        ["provider_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_study_configurations_tag"),
        "study_configurations",
        ["tag"],
        unique=False,
    )
    op.create_index(
        op.f("ix_study_configurations_version"),
        "study_configurations",
        ["version"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_study_configurations_version"), table_name="study_configurations"
    )
    op.drop_index(
        op.f("ix_study_configurations_tag"), table_name="study_configurations"
    )
    op.drop_index(
        op.f("ix_study_configurations_provider_id"), table_name="study_configurations"
    )
    op.drop_index(op.f("ix_study_configurations_id"), table_name="study_configurations")
    op.drop_table("study_configurations")
    # ### end Alembic commands ###
