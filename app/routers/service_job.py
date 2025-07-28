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
    new_service = models.ServiceJob(bike_id=request.bike_id, customer=request.customer,
                                    job_status=request.job_status, priority=request.priority, est_completion=request.est_completion)
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.JobUpdateRequest, db: Session = Depends(get_db)):
    """ Update status or estimated completion of a job """
    job = db.query(models.ServiceJob).filter(
        models.ServiceJob.job_id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service job with id {id} not found")

    if request.job_status:
        db.query(models.ServiceJob).filter(
            models.ServiceJob.job_id == id).update({"job_status": request.job_status})

    if request.est_completion:
        db.query(models.ServiceJob).filter(
            models.ServiceJob.job_id == id).update({"est_completion": request.est_completion})

    db.commit()

    return "updated"


@router.get("/all")
def show_all(db: Session = Depends(get_db)):
    """ Get all service jobs """
    jobs = db.query(models.ServiceJob).all()

    return jobs


@router.get("/completed/count")
def completed_count(db: Session = Depends(get_db)):
    """ Get completed service jobs count """
    completed_jobs = db.query(
        models.ServiceJob).filter_by(job_status="Completed")

    if not completed_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No completed service jobs at the moment")

    return completed_jobs.count()


@router.get("/active/count")
def active_count(db: Session = Depends(get_db)):
    """ Get active service jobs(in progress) count """
    active_jobs = db.query(
        models.ServiceJob).filter_by(job_status="In Progress")

    if not active_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No active service jobs at the moment")

    return active_jobs.count()


@router.get("/pending/count")
def pending_count(db: Session = Depends(get_db)):
    """ Get jobs awaiting service count """
    pending_jobs = db.query(models.ServiceJob).filter_by(job_status="Pending")

    if not pending_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No pending service jobs at the moment")

    return pending_jobs.count()


@router.get("/on-hold/count")
def on_hold_count(db: Session = Depends(get_db)):
    """ Get jobs waiting for parts/approval count """
    jobs_on_hold = db.query(models.ServiceJob).filter_by(job_status="On Hold")

    if not jobs_on_hold:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No jobs on hold at the moment")

    return jobs_on_hold.count()


@router.get("/pending")
def pending(db: Session = Depends(get_db)):
    """ Get pending jobs """
    pending_jobs = db.query(
        models.ServiceJob).filter_by(job_status="Pending").all()

    if not pending_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Pending jobs not found")

    return pending_jobs


@router.get("/in-progress")
def in_progress(db: Session = Depends(get_db)):
    """ Get jobs in progress """
    processing_jobs = db.query(
        models.ServiceJob).filter_by(job_status="In Progress").all()

    if not processing_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Jobs in progress not found")

    return processing_jobs


@router.get("/on-hold")
def on_hold(db: Session = Depends(get_db)):
    """ Get jobs on hold """
    on_hold = db.query(
        models.ServiceJob).filter_by(job_status="On Hold").all()

    if not on_hold:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Jobs on hold not found")

    return on_hold


@router.get("/{id}")
def show(id: int, db: Session = Depends(get_db)):
    """ Get a specific job by job ID"""
    job = db.query(models.ServiceJob).filter(
        models.ServiceJob.job_id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service job with id {id} not found")

    return job


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    """ Delete a job """
    job = db.query(models.ServiceJob).filter(
        models.ServiceJob.job_id == id).delete(synchronize_session=False)

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Service job with id {id} not found")

    db.commit()

    return "deleted"
