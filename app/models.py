# app/models.py

from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.orm import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()

# -------------------------------
# Table 1: store_status
# -------------------------------
class StoreStatus(Base):
    __tablename__ = "store_status"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique row identifier
    store_id = Column(String, nullable=False)  # UUID of the store
    timestamp_utc = Column(DateTime, nullable=False)  # UTC timestamp of the status record
    status = Column(String, nullable=False)  # Store status: "active" or "inactive"


# -------------------------------
# Table 2: store_hours
# -------------------------------
class StoreHours(Base):
    __tablename__ = "store_hours"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique row identifier
    store_id = Column(String, nullable=False)  # UUID of the store
    day = Column(Integer, nullable=False)  # 0 = Monday, ..., 6 = Sunday
    start_time_local = Column(Time, nullable=False)  # Opening time (in store's local time)
    end_time_local = Column(Time, nullable=False)  # Closing time (in store's local time)


# -------------------------------
# Table 3: store_timezone
# -------------------------------
class StoreTimezone(Base):
    __tablename__ = "store_timezone"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique row identifier
    store_id = Column(String, nullable=False, unique=True)  # UUID of the store (1:1 mapping)
    timezone_str = Column(String, nullable=False)  # Timezone string, e.g., "America/Chicago"
