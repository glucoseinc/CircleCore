"""cc_informationsのUUIDをUniqにした

Revision ID: 7cce90c90087
Revises: 62c34208d16c
Create Date: 2019-01-12 13:27:45.327804

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '7cce90c90087'
down_revision = '62c34208d16c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('cc_informations', schema=None) as batch_op:
        batch_op.create_unique_constraint('cstr_ccinfo_uuid_uniq', ['uuid'])


def downgrade():
    with op.batch_alter_table('cc_informations', schema=None) as batch_op:
        batch_op.drop_constraint('cstr_ccinfo_uuid_uniq', type_='unique')
