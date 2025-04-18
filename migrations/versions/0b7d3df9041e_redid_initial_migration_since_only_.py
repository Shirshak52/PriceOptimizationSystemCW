"""Redid initial migration since only Flask Login is being used, not Flask Seurity

Revision ID: 0b7d3df9041e
Revises: 
Create Date: 2025-02-02 22:14:29.190419

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0b7d3df9041e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "supermarket",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=300), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_table(
        "branch",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("location", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=300), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("supermarket_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["supermarket_id"],
            ["supermarket.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_table(
        "dataset_file",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("file_path", sa.String(length=50), nullable=False),
        sa.Column("upload_datetime", sa.DateTime(), nullable=False),
        sa.Column("branch_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["branch_id"],
            ["branch.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_path"),
    )
    op.create_table(
        "optimization",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.String(length=50), nullable=False),
        sa.Column("optimized_price", sa.Float(), nullable=False),
        sa.Column(
            "timeframe", sa.Enum("Weekly", "Monthly", name="timeframes"), nullable=True
        ),
        sa.Column("dataset_file_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_file_id"],
            ["dataset_file.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "prediction",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.String(length=50), nullable=False),
        sa.Column("predicted_sales", sa.Float(), nullable=False),
        sa.Column(
            "timeframe", sa.Enum("Weekly", "Monthly", name="timeframes"), nullable=True
        ),
        sa.Column("dataset_file_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_file_id"],
            ["dataset_file.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "segmentation",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("num_of_clusters", sa.Integer(), nullable=False),
        sa.Column("dataset_file_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_file_id"],
            ["dataset_file.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cluster",
        sa.Column("segmentation_id", sa.UUID(), nullable=False),
        sa.Column("cluster_id", sa.Integer(), nullable=False),
        sa.Column("total_sales", sa.Float(), nullable=False),
        sa.Column("total_qty", sa.Integer(), nullable=False),
        sa.Column("total_visits", sa.Integer(), nullable=False),
        sa.Column("top_product_id", sa.String(length=50), nullable=False),
        sa.Column(
            "timeframe",
            sa.Enum("Weekly", "Monthly", "Quarterly", name="cluster_timeframes"),
            nullable=True,
        ),
        sa.Column("avg_sales_per_timeframe", sa.Float(), nullable=False),
        sa.Column("avg_qty_per_timeframe", sa.Float(), nullable=False),
        sa.Column("avg_visits_per_timeframe", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["segmentation_id"],
            ["segmentation.id"],
        ),
        sa.PrimaryKeyConstraint("segmentation_id", "cluster_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cluster")
    op.drop_table("segmentation")
    op.drop_table("prediction")
    op.drop_table("optimization")
    op.drop_table("dataset_file")
    op.drop_table("branch")
    op.drop_table("supermarket")
    # ### end Alembic commands ###
