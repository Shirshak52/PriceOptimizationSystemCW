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

    # Number of clusters
    num_of_clusters = db.Column(db.Integer, nullable=False)

    # Dataset file ID (Foreign key)
    dataset_file_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dataset_file.id"), nullable=False
    )

    # (Optional) Relationship with DatasetFile
    dataset_file = db.relationship("DatasetFile")
