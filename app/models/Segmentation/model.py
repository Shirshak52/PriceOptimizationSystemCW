import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


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
