"""added 'chosen_metric' to Segmentation, added 'metric_avg' and removed all other columns in Cluster

Revision ID: 300ddfa2b205
Revises: c6364aa72b5b
Create Date: 2025-02-10 22:39:05.816451

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "300ddfa2b205"
down_revision = "c6364aa72b5b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
        CREATE TYPE clustering_metrics AS ENUM (
            'total_visits',
            'total_sales',
            'total_qty',
            'avg_weekly_visits',
            'avg_weekly_sales',
            'avg_weekly_qty',
            'avg_monthly_visits',
            'avg_monthly_sales',
            'avg_monthly_qty',
            'avg_quarterly_visits',
            'avg_quarterly_sales',
            'avg_quarterly_qty'
        );
        """
    )

    with op.batch_alter_table("cluster", schema=None) as batch_op:
        batch_op.add_column(sa.Column("metric_avg", sa.Float(), nullable=False))
        batch_op.drop_column("total_qty")
        batch_op.drop_column("avg_visits_per_timeframe")
        batch_op.drop_column("top_product_id")
        batch_op.drop_column("avg_qty_per_timeframe")
        batch_op.drop_column("avg_sales_per_timeframe")
        batch_op.drop_column("total_sales")
        batch_op.drop_column("timeframe")
        batch_op.drop_column("total_visits")

    with op.batch_alter_table("segmentation", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "chosen_metric",
                sa.Enum(
                    "total_visits",
                    "total_sales",
                    "total_qty",
                    "avg_weekly_visits",
                    "avg_weekly_sales",
                    "avg_weekly_qty",
                    "avg_monthly_visits",
                    "avg_monthly_sales",
                    "avg_monthly_qty",
                    "avg_quarterly_visits",
                    "avg_quarterly_sales",
                    "avg_quarterly_qty",
                    name="clustering_metrics",
                ),
                nullable=False,
            )
        )

    with op.batch_alter_table("supermarket", schema=None) as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sa.VARCHAR(length=5),
            type_=sa.String(length=20),
            existing_nullable=False,
            existing_server_default=sa.text("'admin'::character varying"),
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("supermarket", schema=None) as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sa.String(length=20),
            type_=sa.VARCHAR(length=5),
            existing_nullable=False,
            existing_server_default=sa.text("'admin'::character varying"),
        )

    with op.batch_alter_table("segmentation", schema=None) as batch_op:
        batch_op.drop_column("chosen_metric")

    with op.batch_alter_table("cluster", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("total_visits", sa.INTEGER(), autoincrement=False, nullable=False)
        )
        batch_op.add_column(
            sa.Column(
                "timeframe",
                postgresql.ENUM(
                    "Weekly", "Monthly", "Quarterly", name="cluster_timeframes"
                ),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "total_sales",
                sa.DOUBLE_PRECISION(precision=53),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "avg_sales_per_timeframe",
                sa.DOUBLE_PRECISION(precision=53),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "avg_qty_per_timeframe",
                sa.DOUBLE_PRECISION(precision=53),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "top_product_id",
                sa.VARCHAR(length=50),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "avg_visits_per_timeframe",
                sa.DOUBLE_PRECISION(precision=53),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column("total_qty", sa.INTEGER(), autoincrement=False, nullable=False)
        )
        batch_op.drop_column("metric_avg")

    # ### end Alembic commands ###
