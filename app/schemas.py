from pydantic import BaseModel, model_validator
from datetime import datetime
from enum import Enum
from typing import Optional, Literal


# Service jobs
class JobStatus(str, Enum):
    assigned = "Assigned"
    waiting_parts = "Waiting Parts"
    in_progress = "In Progress"
    completed = "Completed"


class JobUpdateRequest(BaseModel):
    job_status: Optional[Literal["Assigned",
                                 "Waiting Parts", "In Progress", "Completed"]] = None

    deadline: Optional[datetime] = None

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "JobUpdateRequest":
        if not self.job_status and not self.deadline:
            raise ValueError(
                "At least one of 'job_status' or 'deadline' must be provided")

        return self


class ServiceJob(BaseModel):
    customer: str
    job_status: JobStatus
    deadline: datetime      # f"{obj.strftime("%b %d, %Y")}"


# Service requests
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
