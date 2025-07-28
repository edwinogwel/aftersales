from pydantic import BaseModel, model_validator
from datetime import date
from typing import Optional, Literal
from enum import Enum


# Service Jobs
class JobStatus(str, Enum):
    on_hold = "On Hold"
    pending = "Pending"
    assigned = "Assigned"
    in_progress = "In Progress"
    completed = "Completed"


class JobUpdateRequest(BaseModel):
    job_status: Optional[Literal["On Hold", "Pending",
                                 "Assigned", "In Progress", "Completed"]] = None
    est_completion: Optional[date] = None

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "JobUpdateRequest":
        if not self.job_status and not self.est_completion:
            raise ValueError(
                "At least one of 'job_status' or 'est. completion' must be provided")

        return self


class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class ServiceJob(BaseModel):
    bike_id: str
    customer: str
    job_status: JobStatus
    priority: Priority
    # created: automated
    est_completion: date


# Service Requests
class ServiceStatus(str, Enum):
    pending = "Pending"
    scheduled = "Scheduled"
    completed = "Completed"


class ServiceType(str, Enum):
    repair = "Repair"
    maintenance = "Maintenance"
    inspection = "Inspection"


class ServiceRequests(BaseModel):
    customer: str
    bike_id: str
    service_type: ServiceType
    status: ServiceStatus
    submitted: date


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
