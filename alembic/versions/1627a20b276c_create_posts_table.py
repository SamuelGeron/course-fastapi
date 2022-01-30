"""create posts table

Revision ID: 1627a20b276c
Revises: 
Create Date: 2022-01-29 18:13:09.840560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1627a20b276c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.Text, nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
