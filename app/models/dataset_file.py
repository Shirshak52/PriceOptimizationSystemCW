import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app import db


# User class
class DatasetFile(db.Model):
    # Name of table in database
    __tablename__ = "dataset_file"

    # ID
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # File path
    file_path = db.Column(db.String(50), nullable=False, unique=True)

    # Upload datetime
    upload_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Branch ID (Foreign key)
    branch_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("branch.id"), nullable=False
    )

    # (Optional) Relationship with Branch
    branch = db.relationship("Branch")
