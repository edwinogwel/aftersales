from sqlalchemy import Column, Integer, String, Date
from datetime import date
from .database import Base


class ServiceJob(Base):
    __tablename__ = "service-jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    bike_id = Column(String)
    customer = Column(String)
    job_status = Column(String)
    priority = Column(String)
    created = Column(Date, default=(date.today))
    est_completion = Column(Date)


class ServiceRequest(Base):
    __tablename__ = "service-requests"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String)
    bike_id = Column(String)
    service_type = Column(String)
    status = Column(String)
    submitted = Column(Date, default=date.today)


class JobCard(Base):
    __tablename__ = "job-cards"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String)
    contact = Column(Integer)
    date_issued = Column(String)
    bike_id = Column(String)
    # Vehicle info
    odometer_reading = Column(String)
    bike_model = Column(String)
    license_plate = Column(String)
    service_type = Column(String)
    issue_description = Column(String)
    # Parts required -> should allow multiple entries
    part_no = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)
