from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models
from typing import Optional


router = APIRouter(
    prefix="/service-requests",
    tags=["service-requests"]
)

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.ServiceRequests, db: Session = Depends(get_db)):
    """ Submit a new request """
    new_request = models.ServiceRequest(customer=request.customer, bike_id=request.bike_id,
                                        service_type=request.service_type, status=request.status)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, service_status: Optional[str] = None, db: Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == id).first()

    if not service_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service request with id {id} not found")

    if service_status:
        db.query(models.ServiceRequest).filter(
            models.ServiceRequest.id == id).update({"status": service_status})

    db.commit()

    return "updated"


@router.get("/pending")
def pending_request(db: Session = Depends(get_db)):
    pending_requests = db.query(
        models.ServiceRequest).filter_by(status="Pending")

    if not pending_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no pending requests at the moment")

    return pending_requests.count()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == id).delete(synchronize_session=False)

    if not service_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service request with id {id} not found")

    db.commit()

    return "deleted"
