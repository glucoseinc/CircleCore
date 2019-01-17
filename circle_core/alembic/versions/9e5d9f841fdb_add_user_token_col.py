"""empty message

Revision ID: 9e5d9f841fdb
Revises: 7cce90c90087
Create Date: 2019-01-12 13:37:56.484550

"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9e5d9f841fdb'
down_revision = '7cce90c90087'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.Binary(), nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('token')
