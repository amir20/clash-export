"""empty message

Revision ID: 31afd2859504
Revises: 8e79948e21ac
Create Date: 2019-01-05 18:07:44.740205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '31afd2859504'
down_revision = '8e79948e21ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('achievements', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('player', sa.Column('attackWins', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('bestTrophies', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('bestVersusTrophies', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('builderHallLevel', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('defenseWins', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('donations', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('donationsReceived', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('expLevel', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('heroes', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('player', sa.Column('league', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('player', sa.Column('legendStatistics', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('player', sa.Column('role', sa.String(length=20), nullable=True))
    op.add_column('player', sa.Column('spells', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('player', sa.Column('townHallLevel', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('townHallWeaponLevel', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('troops', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('player', sa.Column('trophies', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('versusBattleWinCount', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('versusBattleWins', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('versusTrophies', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('warStars', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('player', 'warStars')
    op.drop_column('player', 'versusTrophies')
    op.drop_column('player', 'versusBattleWins')
    op.drop_column('player', 'versusBattleWinCount')
    op.drop_column('player', 'trophies')
    op.drop_column('player', 'troops')
    op.drop_column('player', 'townHallWeaponLevel')
    op.drop_column('player', 'townHallLevel')
    op.drop_column('player', 'spells')
    op.drop_column('player', 'role')
    op.drop_column('player', 'legendStatistics')
    op.drop_column('player', 'league')
    op.drop_column('player', 'heroes')
    op.drop_column('player', 'expLevel')
    op.drop_column('player', 'donationsReceived')
    op.drop_column('player', 'donations')
    op.drop_column('player', 'defenseWins')
    op.drop_column('player', 'builderHallLevel')
    op.drop_column('player', 'bestVersusTrophies')
    op.drop_column('player', 'bestTrophies')
    op.drop_column('player', 'attackWins')
    op.drop_column('player', 'achievements')
    # ### end Alembic commands ###
