from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models


router = APIRouter(
    prefix="/service-jobs",
    tags=["service-jobs"]
)

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.ServiceJob, db: Session = Depends(get_db)):
    """ Create a new service job """
    new_service = models.ServiceJob(
        customer=request.customer, job_status=request.job_status, deadline=request.deadline)
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(job_id: int, request: schemas.JobUpdateRequest, db: Session = Depends(get_db)):
    """ Update status or deadline of a job """
    job = db.query(models.ServiceJob).filter(
        models.ServiceJob.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service job with id {id} not found")

    if request.job_status:
        db.query(models.ServiceJob).filter(
            models.ServiceJob.job_id == job_id).update({"job_status": request.job_status})

    if request.deadline:
        db.query(models.ServiceJob).filter(
            models.ServiceJob.job_id == job_id).update({"deadline": request.deadline})

    db.commit()

    return "updated"


@router.get("/all")
def show_all(db: Session = Depends(get_db)):
    """ Get all active jobs """
    jobs = db.query(models.ServiceJob).all()

    return jobs


@router.get("/completed")
def completed_jobs(db: Session = Depends(get_db)):
    """ Get completed service jobs count """
    completed_jobs = db.query(
        models.ServiceJob).filter_by(job_status="Completed")

    if not completed_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no completed service jobs at the moment")

    return completed_jobs.count()


@router.get("/active")
def active_jobs(db: Session = Depends(get_db)):
    """ Get active service jobs count """
    active_statuses = ["Assigned", "Waiting Parts", "In Progress"]

    active_jobs = db.query(
        models.ServiceJob).filter(models.ServiceJob.job_status.in_(active_statuses))

    if not active_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no active service jobs at the moment")

    return active_jobs.count()


@router.get("/{id}")
def show(job_id: int, db: Session = Depends(get_db)):
    """ Get a specific job by ID"""
    job = db.query(models.ServiceJob).filter(
        models.ServiceJob.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service job with id {id} not found")

    return job


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(job_id: int, db: Session = Depends(get_db)):
    """ Delete a job """
    job = db.query(models.ServiceJob).filter(
        models.ServiceJob.job_id == job_id).delete(synchronize_session=False)

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service job with id {id} not found")

    db.commit()

    return "deleted"
