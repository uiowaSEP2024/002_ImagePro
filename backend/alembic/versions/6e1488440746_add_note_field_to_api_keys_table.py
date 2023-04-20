"""Add Note field to API Keys table

Revision ID: 6e1488440746
Revises: 97c85d02b221
Create Date: 2023-04-20 01:42:25.121528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e1488440746'
down_revision = '97c85d02b221'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_keys', sa.Column('note', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_keys', 'note')
    # ### end Alembic commands ###
