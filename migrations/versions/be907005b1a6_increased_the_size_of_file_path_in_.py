"""increased the size of 'file_path' in DatasetFile

Revision ID: be907005b1a6
Revises: 300ddfa2b205
Create Date: 2025-02-15 21:04:19.437403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be907005b1a6'
down_revision = '300ddfa2b205'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dataset_file', schema=None) as batch_op:
        batch_op.alter_column('file_path',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dataset_file', schema=None) as batch_op:
        batch_op.alter_column('file_path',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
