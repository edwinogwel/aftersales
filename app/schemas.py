from pydantic import BaseModel, model_validator
from datetime import date
from typing import Optional, Literal
from enum import Enum


# Service Job
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


class JobStatus(str, Enum):
    on_hold = "On Hold"
    pending = "Pending"
    assigned = "Assigned"
    in_progress = "In Progress"
    completed = "Completed"


class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    urgent = "Urgent"


class ServiceJob(BaseModel):
    bike_id: str
    customer: str
    job_status: JobStatus
    priority: Priority
    est_completion: date


# Service Request
class ServiceUpdateRequest(BaseModel):
    service_status: Optional[Literal["New", "Waiting for Customer",
                                     "Waiting for Parts", "In Progress", "Resolved"]] = None


class ServiceType(str, Enum):
    repair = "Repair"
    maintenance = "Regular Maintenance"
    inspection = "Technical Inspection"
    upgrade = "Component Upgrade"


class ServiceStatus(str, Enum):
    new = "New"
    pending_customer = "Waiting for Customer"
    pending_parts = "Waiting for Parts"
    scheduled = "In Progress"
    resolved = "Resolved"


class ServiceRequests(BaseModel):
    bike_id: str
    customer: str
    service_type: ServiceType
    priority: Priority
    status: ServiceStatus
    problem_description: str
    request_date: date
    customer_phone: int
    additional_notes: Optional[str]
    last_updated: date


# Part Inventory
class PartCategory(str, Enum):
    components = "Components"
    electrical = "Electrical"
    mechanical = "Mechanical"


class StockStatus(str, Enum):
    low_stock = "Low Stock"
    in_stock = "In Stock"
    out_of_stock = "Out of Stock"


class PartInventory(BaseModel):
    part_name: str
    category: PartCategory
    quantity: int
    location: str
    supplier: str
    unit_price: float
    # stock_status: Optional[StockStatus] = None  # auto-set

    # class Config:
    #     orm_mode = True


# Job Card
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
