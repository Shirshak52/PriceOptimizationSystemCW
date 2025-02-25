import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


class OptimizedPrices(db.Model):
    # Name of table in database
    __tablename__ = "optimized_prices"

    # PRIMARY KEY START=================================================
    # Optimization ID (Foreign key)
    optimization_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("optimization.id"), primary_key=True
    )

    # Timeframe
    timeframe = db.Column(
        db.Enum("Next Week", "Next Month", "Next Quarter", name="opt_timeframes"),
        primary_key=True,
    )

    # Product ID from the uploaded dataset
    product_id = db.Column(db.String(100), primary_key=True)

    # Composite primary key: (optimization_id, timeframe, product_id)
    __table_args__ = (
        db.PrimaryKeyConstraint("optimization_id", "timeframe", "product_id"),
    )
    # PRIMARY KEY END=================================================

    # Predicted prices and optimized prices
    predicted_prices = db.Column(db.Float, nullable=False)
    optimized_prices = db.Column(db.Float, nullable=False)
