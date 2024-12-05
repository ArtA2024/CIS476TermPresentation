"""Added Identity fields

Revision ID: 89aec76eade3
Revises: 6114f64d2d92
Create Date: 2024-12-04 19:54:47.261173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89aec76eade3'
down_revision = '6114f64d2d92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vault_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('passport_number', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('driver_license', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('ssn', sa.String(length=11), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vault_item', schema=None) as batch_op:
        batch_op.drop_column('ssn')
        batch_op.drop_column('driver_license')
        batch_op.drop_column('passport_number')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('address')
        batch_op.drop_column('full_name')

    # ### end Alembic commands ###
