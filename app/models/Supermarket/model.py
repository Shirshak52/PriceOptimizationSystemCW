import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db


# Admin class
class Supermarket(db.Model):
    # Name of table in database
    __tablename__ = "supermarket"

    # ID
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Name
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Phone number
    phone_number = db.Column(db.String(15), nullable=False, unique=True)

    # Email
    email = db.Column(db.String(100), nullable=False, unique=True)

    # Password
    password = db.Column(db.String(300), nullable=False)

    # Role
    role = db.Column(db.String(20), nullable=False, default="admin")  # Admin or user
