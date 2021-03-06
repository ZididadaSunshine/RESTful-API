"""added posts to brand

Revision ID: bb89c6ef11c0
Revises: 1dc6121fa692
Create Date: 2018-12-11 12:04:17.772769

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bb89c6ef11c0'
down_revision = '1dc6121fa692'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('brand', sa.Column('posts', sa.Integer(), nullable=True))
    op.add_column('brand', sa.Column('statistics_updated_at', sa.DateTime(), nullable=True))
    op.drop_column('brand', 'sentiment_updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('brand', sa.Column('sentiment_updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('brand', 'statistics_updated_at')
    op.drop_column('brand', 'posts')
    # ### end Alembic commands ###
