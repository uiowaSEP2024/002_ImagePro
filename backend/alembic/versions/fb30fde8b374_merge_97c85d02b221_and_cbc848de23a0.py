"""merge 97c85d02b221 and cbc848de23a0

Revision ID: fb30fde8b374
Revises: 97c85d02b221, cbc848de23a0
Create Date: 2023-04-22 18:28:18.915591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fb30fde8b374"
down_revision = ("97c85d02b221", "cbc848de23a0")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
