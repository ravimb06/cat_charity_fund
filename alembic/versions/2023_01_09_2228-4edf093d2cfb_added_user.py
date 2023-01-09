"""Added User

Revision ID: 4edf093d2cfb
Revises: 520e2d6c0da5
Create Date: 2023-01-09 22:28:07.952406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4edf093d2cfb'
down_revision = '520e2d6c0da5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('donation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donation',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('full_amount', sa.INTEGER(), nullable=False),
    sa.Column('invested_amount', sa.INTEGER(), nullable=True),
    sa.Column('fully_invested', sa.BOOLEAN(), nullable=True),
    sa.Column('create_date', sa.DATETIME(), nullable=True),
    sa.Column('close_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
