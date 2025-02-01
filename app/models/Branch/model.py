from flask_security import UserMixin
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db


# User class
class Branch(db.Model, UserMixin):
    # Name of table in database
    __tablename__ = "branch"

    # ID
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # fs-uniquifier (for Flask-Security 4.0+)
    fs_uniquifier = db.Column(
        db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    # Name
    name = db.Column(db.String(50), nullable=False)

    # Location
    location = db.Column(db.String(100), nullable=False)

    # Phone number
    phone_number = db.Column(db.String(15), nullable=False, unique=True)

    # Email
    email = db.Column(db.String(100), nullable=False, unique=True)

    # Password
    password = db.Column(db.String(300), nullable=False)

    # Status
    active = db.Column(db.Boolean, default=True)

    # Role
    role = db.Column(db.String(20), nullable=False, default="user")  # Admin or user

    # Supermarket ID (Foreign key)
    supermarket_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("supermarket.id"), nullable=False
    )

    # (Optional) Relationship with Supermarket
    supermarket = db.relationship("Supermarket")
