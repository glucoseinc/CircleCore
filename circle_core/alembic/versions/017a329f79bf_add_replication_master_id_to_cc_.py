"""add `replication_master_id` to cc_informations

Revision ID: 017a329f79bf
Revises:
Create Date: 2017-02-13 21:36:56.994225

"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '017a329f79bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cc_informations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('replication_master_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_cc_informations_replication_masters', 'replication_masters', ['replication_master_id'],
            ['replication_master_id']
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cc_informations', schema=None) as batch_op:
        batch_op.drop_constraint('fk_cc_informations_replication_masters', type_='foreignkey')
        batch_op.drop_column('replication_master_id')

    # ### end Alembic commands ###
