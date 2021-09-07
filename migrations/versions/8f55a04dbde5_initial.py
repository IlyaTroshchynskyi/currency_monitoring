"""initial

Revision ID: 8f55a04dbde5
Revises: 
Create Date: 2021-09-07 22:54:52.137107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f55a04dbde5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('x_rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_currency', sa.Integer(), nullable=True),
    sa.Column('to_currency', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_x_rate_from_currency'), 'x_rate', ['from_currency'], unique=False)
    op.create_index(op.f('ix_x_rate_to_currency'), 'x_rate', ['to_currency'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_x_rate_to_currency'), table_name='x_rate')
    op.drop_index(op.f('ix_x_rate_from_currency'), table_name='x_rate')
    op.drop_table('x_rate')
    # ### end Alembic commands ###
