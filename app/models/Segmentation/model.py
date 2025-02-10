import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db


# User class
class Segmentation(db.Model):
    # Name of table in database
    __tablename__ = "segmentation"

    # ID
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Metric chosen for clustering
    chosen_metric = db.Column(
        db.Enum(
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

    # Number of clusters
    num_of_clusters = db.Column(db.Integer, nullable=False)

    # Dataset file ID (Foreign key)
    dataset_file_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dataset_file.id"), nullable=False
    )

    # (Optional) Relationship with DatasetFile
    dataset_file = db.relationship("DatasetFile")
