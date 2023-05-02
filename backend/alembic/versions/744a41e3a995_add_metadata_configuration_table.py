"""Add Metadata Configuration Table

Revision ID: 744a41e3a995
Revises: fbdb84d6f575
Create Date: 2023-04-30 21:44:36.159586

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "744a41e3a995"
down_revision = "fbdb84d6f575"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "metadata_configurations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "kind",
            sa.Enum("text", "number", "link", name="metadata_kind"),
            server_default="text",
            nullable=False,
        ),
        sa.Column("units", sa.String(), nullable=True),
        sa.Column("step_configuration_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["step_configuration_id"],
            ["step_configurations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_metadata_configurations_id"),
        "metadata_configurations",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_metadata_configurations_name"),
        "metadata_configurations",
        ["name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_metadata_configurations_step_configuration_id"),
        "metadata_configurations",
        ["step_configuration_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_metadata_configurations_step_configuration_id"),
        table_name="metadata_configurations",
    )
    op.drop_index(
        op.f("ix_metadata_configurations_name"), table_name="metadata_configurations"
    )
    op.drop_index(
        op.f("ix_metadata_configurations_id"), table_name="metadata_configurations"
    )
    op.drop_table("metadata_configurations")
    sa.Enum("text", "number", "link", name="metadata_kind").drop(
        op.get_bind(), checkfirst=False
    )
