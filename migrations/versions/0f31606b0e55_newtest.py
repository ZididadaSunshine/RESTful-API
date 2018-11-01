"""newtest

Revision ID: 0f31606b0e55
Revises: 
Create Date: 2018-11-01 10:33:52.675760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f31606b0e55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('invalid_token',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('synonym',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('synonym', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('synonym')
    )
    op.create_table('brand',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brand_synonym',
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('synonym_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['synonym_id'], ['synonym.id'], ),
    sa.PrimaryKeyConstraint('brand_id', 'synonym_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('brand_synonym')
    op.drop_table('brand')
    op.drop_table('synonym')
    op.drop_table('invalid_token')
    op.drop_table('account')
    # ### end Alembic commands ###
