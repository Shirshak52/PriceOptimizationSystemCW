"""Added 'cluster_counts' to Cluster

Revision ID: 5c03d50d7ad6
Revises: be907005b1a6
Create Date: 2025-02-21 21:30:13.683158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c03d50d7ad6'
down_revision = 'be907005b1a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cluster', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cluster_count', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cluster', schema=None) as batch_op:
        batch_op.drop_column('cluster_count')

    # ### end Alembic commands ###
