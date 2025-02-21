import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


# User class
class Optimization(db.Model):
    # Name of table in database
    __tablename__ = "optimization"

    # ID
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Product ID
    product_id = db.Column(db.String(50), nullable=False)

    # Optimized price
    optimized_price = db.Column(db.Float, nullable=False)

    # Timeframe (Weekly/Monthly)
    timeframe = db.Column(db.Enum("Weekly", "Monthly", name="timeframes"))

    # Dataset file ID (Foreign key)
    dataset_file_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dataset_file.id"), nullable=False
    )

    # (Optional) Relationship with DatasetFile
    dataset_file = db.relationship("DatasetFile")
