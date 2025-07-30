from sqlalchemy import Column, Integer, String, Date, Float
from datetime import date
from .database import Base


class ServiceJob(Base):
    __tablename__ = "service-jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    bike_id = Column(String, unique=True)
    customer = Column(String)
    job_status = Column(String)
    priority = Column(String)
    created = Column(Date, default=(date.today))
    est_completion = Column(Date)


class ServiceRequest(Base):
    __tablename__ = "service-requests"

    id = Column(Integer, primary_key=True, index=True)
    bike_id = Column(String, unique=True)
    customer = Column(String)
    service_type = Column(String)
    priority = Column(String)
    status = Column(String)
    problem_description = Column(String)
    created = Column(Date, default=date.today)
    request_date = Column(Date)
    customer_phone = Column(Integer)
    additional_notes = Column(String, default="")
    last_updated = Column(Date)


class PartInventory(Base):
    __tablename__ = "parts-inventory"

    id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String)
    category = Column(String)
    stock_status = Column(String)
    quantity = Column(Integer)
    location = Column(String)
    supplier = Column(String)
    unit_price = Column(Float)


class JobCard(Base):
    __tablename__ = "job-cards"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String)
    contact = Column(Integer)
    date_issued = Column(String)
    bike_id = Column(String, unique=True)
    # Vehicle info
    odometer_reading = Column(String)
    bike_model = Column(String)
    license_plate = Column(String, unique=True)
    service_type = Column(String)
    issue_description = Column(String)
    # Parts required -> should allow multiple entries
    part_no = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)
