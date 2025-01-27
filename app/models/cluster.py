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
    # Total sales
    total_sales = db.Column(db.Float, nullable=False)

    # Total quantity
    total_qty = db.Column(db.Integer, nullable=False)

    # Total visits
    total_visits = db.Column(db.Integer, nullable=False)

    # Top product ID
    top_product_id = db.Column(db.String(50), nullable=False)

    # Timeframe for averages
    timeframe = db.Column(
        db.Enum("Weekly", "Monthly", "Quarterly", name="cluster_timeframes")
    )
    # Average sales per timeframe
    avg_sales_per_timeframe = db.Column(db.Float, nullable=False)

    # Average quantity per timeframe
    avg_qty_per_timeframe = db.Column(db.Float, nullable=False)

    # Average visits per timeframe
    avg_visits_per_timeframe = db.Column(db.Float, nullable=False)
    # CLUSTER PROFILE DATA END=================================================

    # (Optional) Relationship with Segmentation
    segmentation = db.relationship("Segmentation")
