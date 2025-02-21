import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db


# User class
class Cluster(db.Model):
    # Name of table in database
    __tablename__ = "cluster"

    # PRIMARY KEY START=================================================
    # Segmentation ID (Foreign key)
    segmentation_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("segmentation.id"), primary_key=True
    )

    # Cluster ID
    cluster_id = db.Column(
        db.Integer,
        primary_key=True,
    )

    # Composite primary key: (segmentation_id, cluster_id)
    __table_args__ = (db.PrimaryKeyConstraint("segmentation_id", "cluster_id"),)
    # PRIMARY KEY END=================================================

    # CLUSTER PROFILE DATA START=================================================
    # Number of customers inside the cluster
    cluster_count = db.Column(db.Integer, nullable=False)

    # Average value of the chosen clustering metric
    metric_avg = db.Column(db.Float, nullable=False)
    # CLUSTER PROFILE DATA END=================================================

    # (Optional) Relationship with Segmentation
    segmentation = db.relationship("Segmentation")
