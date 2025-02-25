import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


# User class
class Prediction(db.Model):
    # Name of table in database
    __tablename__ = "prediction"

    # ID
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Predicted sales amounts
    sales_next_week = db.Column(db.Float, nullable=False)
    sales_next_month = db.Column(db.Float, nullable=False)
    sales_next_quarter = db.Column(db.Float, nullable=False)

    # Dataset file ID (Foreign key)
    dataset_file_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dataset_file.id"), nullable=False
    )

    # (Optional) Relationship with DatasetFile
    dataset_file = db.relationship("DatasetFile")
