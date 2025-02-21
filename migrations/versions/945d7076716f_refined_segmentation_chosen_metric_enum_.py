"""Refined Segmentation.chosen_metric ENUM values to match those in SegmentationParametersForm.chosen_metric, and renamed the ENUM from clustering_metrics to segmentation_metrics

Revision ID: 945d7076716f
Revises: 5c03d50d7ad6
Create Date: 2025-02-21 23:08:50.411126

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "945d7076716f"
down_revision = "5c03d50d7ad6"
branch_labels = None
depends_on = None

new_enum = sa.Enum(
    "Total Visits",
    "Total Sales",
    "Total Quantity",
    "Average Weekly Visits",
    "Average Weekly Sales",
    "Average Weekly Quantity",
    "Average Monthly Visits",
    "Average Monthly Sales",
    "Average Monthly Quantity",
    "Average Quarterly Visits",
    "Average Quarterly Sales",
    "Average Quarterly Quantity",
    name="segmentation_metrics",
)

old_enum = sa.Enum(
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
)


def upgrade():
    # Create the new ENUM
    new_enum.create(op.get_bind(), checkfirst=True)

    # Alter the column to use the new ENUM type
    op.execute(
        "ALTER TABLE segmentation ALTER COLUMN chosen_metric TYPE segmentation_metrics USING chosen_metric::text::segmentation_metrics"
    )

    # Drop the old ENUM type
    op.execute("DROP TYPE clustering_metrics")


def downgrade():
    # Recreate the new ENUM
    old_enum.create(op.get_bind(), checkfirst=True)

    # Revert the column back to the old ENUM type
    op.execute(
        "ALTER TABLE segmentation ALTER COLUMN chosen_metric TYPE clustering_metrics USING chosen_metric::text::clustering_metrics"
    )

    # Drop the new ENUM type
    op.execute("DROP TYPE segmentation_metrics")
