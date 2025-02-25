import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


class Optimization(db.Model):
    # Name of table in database
    __tablename__ = "optimization"

    # ID
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Dataset file ID (Foreign key)
    dataset_file_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dataset_file.id"), nullable=False
    )

    # (Optional) Relationship with DatasetFile
    dataset_file = db.relationship("DatasetFile")

    # Relationships with OptimizedSales and OptimizedPrices
    optimized_sales = db.relationship(
        "OptimizedSales", backref="optimization", cascade="all, delete-orphan"
    )
    optimized_prices = db.relationship(
        "OptimizedPrices", backref="optimization", cascade="all, delete-orphan"
    )
