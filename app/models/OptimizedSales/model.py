import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


class OptimizedSales(db.Model):
    # Name of table in database
    __tablename__ = "optimized_sales"

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

    # Composite primary key: (optimization_id, timeframe)
    __table_args__ = (db.PrimaryKeyConstraint("optimization_id", "timeframe"),)
    # PRIMARY KEY END=================================================

    # Predicted sales and optimized sales
    predicted_sales = db.Column(db.Float, nullable=False)
    optimized_sales = db.Column(db.Float, nullable=False)
