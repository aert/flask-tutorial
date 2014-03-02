"""add_aboutme_lastseen

Revision ID: 1564f1d4b8f
Revises: 57ebbe762de8
Create Date: 2014-03-02 19:34:15.613414

"""

# revision identifiers, used by Alembic.
revision = '1564f1d4b8f'
down_revision = '57ebbe762de8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=180), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    ### end Alembic commands ###
