"""Create api keys table

Revision ID: 19eb77a561bd
Revises: 327021060de9
Create Date: 2023-03-04 12:09:08.789488

"""
from alembic import op
import sqlalchemy as sa

revision = "19eb77a561bd"
down_revision = "327021060de9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "api_keys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("key", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_index(op.f("ix_api_keys_id"), "api_keys", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_api_keys_id"), table_name="api_keys")
    op.drop_table("api_keys")
