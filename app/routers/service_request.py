from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models


router = APIRouter(
    prefix="/service-requests",
    tags=["service-requests"]
)

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.ServiceRequests, db: Session = Depends(get_db)):
    """ Submit a new service request """
    new_request = models.ServiceRequest(bike_id=request.bike_id, customer=request.customer, service_type=request.service_type, priority=request.priority, status=request.status,
                                        problem_description=request.problem_description, request_date=request.request_date, customer_phone=request.customer_phone, additional_notes=request.additional_notes, last_updated=request.last_updated)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.ServiceUpdateRequest, db: Session = Depends(get_db)):
    """ Update service request status """
    service_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == id).first()

    if not service_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service request with id {id} not found")

    if request.service_status:
        db.query(models.ServiceRequest).filter(
            models.ServiceRequest.id == id).update({"status": request.service_status})

    db.commit()

    return "updated"


@router.get("/all")
def show_all(db: Session = Depends(get_db)):
    """ Get all service requests """
    service_requests = db.query(models.ServiceRequest).all()

    if not service_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Service requests not found")

    return service_requests


@router.get("/new/count")
def new_count(db: Session = Depends(get_db)):
    """ Get requests that require attention count """
    new_requests = db.query(models.ServiceRequest).filter_by(status="New")

    if not new_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="New service requests not found")

    return new_requests.count()


@router.get("/in-progress/count")
def in_progress_count(db: Session = Depends(get_db)):
    """ Get requests that are being processed count """
    processing_requests = db.query(
        models.ServiceRequest).filter_by(status="In Progress")

    if not processing_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Service requests in progress not found")

    return processing_requests.count()


@router.get("/waiting/count")
def pending_count(db: Session = Depends(get_db)):
    """ Get requests waiting for parts or customer count """
    pending_statuses = ["Waiting for Customer", "Waiting for Parts"]

    pending_requests = db.query(
        models.ServiceRequest).filter(models.ServiceRequest.status.in_(pending_statuses))

    if not pending_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Pending service requests not found")

    return pending_requests.count()


@router.get("/new")
def new(db: Session = Depends(get_db)):
    """ Get new requests """
    new_requests = db.query(
        models.ServiceRequest).filter_by(status="New").all()

    if not new_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="New requests not found")

    return new_requests


@router.get("/in-progress")
def in_progress(db: Session = Depends(get_db)):
    """ Get requests in progress """
    processing_requests = db.query(
        models.ServiceRequest).filter_by(status="In Progress").all()

    if not processing_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Service requests in progress not found")

    return processing_requests


@router.get("/waiting-for-parts")
def waiting_for_parts(db: Session = Depends(get_db)):
    """ Get requests waiting for parts """
    waiting_parts = db.query(
        models.ServiceRequest).filter_by(status="Waiting for Parts").all()

    if not waiting_parts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Requests waiting for parts not found")

    return waiting_parts


@router.get("/waiting-for-customer")
def waiting_for_customer(db: Session = Depends(get_db)):
    """ Get requests waiting for customer """
    waiting_customer = db.query(
        models.ServiceRequest).filter_by(status="Waiting for Customer").all()

    if not waiting_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Requests waiting for customer not found")

    return waiting_customer


@router.get("/resolved")
def resolved(db: Session = Depends(get_db)):
    """ Get resolved requests """
    resolved_requests = db.query(
        models.ServiceRequest).filter_by(status="Resolved").all()

    if not resolved_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Resolved requests not found")

    return resolved_requests


@router.get("/{id}")
def show(id: int, db: Session = Depends(get_db)):
    """ Get specific service request """
    service_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == id).first()

    if not service_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service request with id {id} not found")

    return service_request


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    """ Delete a service request """
    service_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == id).delete(synchronize_session=False)

    if not service_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service request with id {id} not found")

    db.commit()

    return "deleted"
