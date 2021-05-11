"""empty message

Revision ID: 192f883cc999
Revises: 
Create Date: 2021-03-22 05:03:22.345107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '192f883cc999'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('challenger_username', sa.String(length=255), nullable=False),
    sa.Column('opponent_username', sa.String(length=255), nullable=False),
    sa.Column('current_player', sa.String(length=255), nullable=False),
    sa.Column('winner', sa.String(length=255), nullable=True),
    sa.Column('can_move', sa.Boolean(), nullable=True),
    sa.Column('board', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players')
    op.drop_table('Games')
    # ### end Alembic commands ###