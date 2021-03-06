"""empty message

Revision ID: b6f52b86a3b1
Revises: 08c5b4124c1d
Create Date: 2017-03-05 23:18:51.430205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6f52b86a3b1'
down_revision = '08c5b4124c1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    # ### end Alembic commands ###
