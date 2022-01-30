"""Add content column to posts table

Revision ID: eb88fb6db092
Revises: 1627a20b276c
Create Date: 2022-01-29 18:22:19.129542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb88fb6db092'
down_revision = '1627a20b276c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.Text, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
