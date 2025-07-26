from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    assigned = "Assigned"
    waiting_parts = "Waiting Parts"
    in_progress = "In Progress"
    completed = "Completed"


class ServiceJob(BaseModel):
    customer: str
    job_status: JobStatus
    deadline: datetime      # f"{obj.strftime("%b %d, %Y")}"


class ServiceRequests(BaseModel):
    customer: str
    bike_id: str
    service_type: str
    status: str
    submitted: datetime


class JobCard(BaseModel):
    customer: str
    contact: int
    date_issued: str
    bike_id: str
    # Vehicle info
    odometer_reading: str
    bike_model: str
    license_plate: str
    service_type: str
    issue_description: str
    # Parts required -> should allow multiple entries
    part_no: int
    quantity: int
    price: int
