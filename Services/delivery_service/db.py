
import os
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# Override with PostgreSQL via DATABASE_URL env var:
# DATABASE_URL=postgresql://user:password@host:5432/deliverydb

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/deliverydb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Delivery(Base):
    """Represents a single package delivery assignment to a driver."""
    __tablename__ = "deliveries"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    order_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    driver_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    package_id: Mapped[str] = mapped_column(String, nullable=False)
    delivery_address: Mapped[str] = mapped_column(String, nullable=False)
    # Possible statuses: assigned | in_transit | delivered | failed
    status: Mapped[str] = mapped_column(String, default="assigned", nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)

class DeliveryFeedback(Base):
    """Proof-of-delivery record submitted by the driver."""
    __tablename__ = "delivery_feedback"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    delivery_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    # delivered | failed
    status: Mapped[str] = mapped_column(String, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # Base-64 encoded digital signature supplied by driver
    signature_data: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # URL / path to uploaded photo proof
    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)