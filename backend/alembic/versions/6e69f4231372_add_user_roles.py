"""Add user roles

Revision ID: 6e69f4231372
Revises: b6bcaa15f3ed
Create Date: 2023-04-26 00:54:59.050977

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6e69f4231372"
down_revision = "b6bcaa15f3ed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    postgresql.ENUM("provider", "customer", name="user_role").create(op.get_bind())
    op.add_column(
        "users",
        sa.Column(
            "role", sa.Enum("provider", "customer", name="user_role"), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "role")
    sa.Enum("provider", "customer", name="user_role").drop(
        op.get_bind(), checkfirst=False
    )
