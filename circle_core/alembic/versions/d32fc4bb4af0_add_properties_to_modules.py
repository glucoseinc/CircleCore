"""empty message

Revision ID: d32fc4bb4af0
Revises: 0b8528a90b40
Create Date: 2017-02-21 17:27:31.434608

"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd32fc4bb4af0'
down_revision = '0b8528a90b40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('modules', schema=None) as batch_op:
        batch_op.add_column(sa.Column('properties', sa.TEXT(), nullable=False, server_default=''))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('modules', schema=None) as batch_op:
        batch_op.drop_column('properties')

    # ### end Alembic commands ###
