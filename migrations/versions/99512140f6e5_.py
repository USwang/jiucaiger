"""empty message

Revision ID: 99512140f6e5
Revises: ba7d2d5e407f
Create Date: 2024-01-12 09:21:22.120999

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '99512140f6e5'
down_revision = 'ba7d2d5e407f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jcgstockdata',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('SECURITY_CODE', sa.String(length=50), nullable=True),
    sa.Column('SECURITY_NAME_ABBR', sa.String(length=50), nullable=True),
    sa.Column('PRICE_datajson', sa.JSON(), nullable=True),
    sa.Column('INCOME_datajson', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('SECURITY_CODE')
    )
    with op.batch_alter_table('stockdata', schema=None) as batch_op:
        batch_op.drop_index('SECURITY_CODE')

    op.drop_table('stockdata')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stockdata',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('SECURITY_CODE', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('SECURITY_NAME_ABBR', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('INCOME_datajson', mysql.JSON(), nullable=True),
    sa.Column('PRICE_datajson', mysql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('stockdata', schema=None) as batch_op:
        batch_op.create_index('SECURITY_CODE', ['SECURITY_CODE'], unique=False)

    op.drop_table('jcgstockdata')
    # ### end Alembic commands ###
