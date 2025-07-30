from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .helpers import determine_stock_status

router = APIRouter(
    prefix="/parts",
    tags=["parts"]
)

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.PartInventory, db: Session = Depends(get_db)):
    """ Add new part to inventory """
    status = determine_stock_status(request.quantity)

    new_model = models.PartInventory(
        part_name=request.part_name,
        category=request.category,
        stock_status=status.value,
        quantity=request.quantity,
        location=request.location,
        supplier=request.supplier,
        unit_price=request.unit_price
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return new_model


@router.get("/all")
def show_all(db: Session = Depends(get_db)):
    """ Get all parts """
    parts = db.query(models.PartInventory).all()

    if not parts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parts not found")

    return parts


@router.get("/in-stock/count")
def in_stock_count(db: Session = Depends(get_db)):
    """ Get parts in stock count """
    in_stock = db.query(models.PartInventory).filter_by(
        stock_status="In Stock")

    if not in_stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parts in stock not found")

    return in_stock.count()


@router.get("/out-of-stock/count")
def out_of_stock_count(db: Session = Depends(get_db)):
    """ Get parts out of stock count """
    out_of_stock = db.query(models.PartInventory).filter_by(
        stock_status="Out of Stock")

    if not out_of_stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parts out of stock not found")

    return out_of_stock.count()


@router.get("/low-stock/count")
def low_stock_count(db: Session = Depends(get_db)):
    """ Get parts with low stock count """
    low_stock = db.query(models.PartInventory).filter_by(
        stock_status="Low Stock")

    if not low_stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parts with low stock not found")

    return low_stock.count()


@router.get("/in-stock/percent")
def in_stock_percent(db: Session = Depends(get_db)):
    """ Get percent of total inventory in stock """
    total = db.query(models.PartInventory).count()
    in_stock = db.query(models.PartInventory).filter_by(
        stock_status="In Stock").count()

    percent_in_stock = (in_stock / total) * 100

    return f"{int(percent_in_stock)}% of total inventory"


@router.get("/out-of-stock/percent")
def out_of_stock_percent(db: Session = Depends(get_db)):
    """ Get percent of total inventory out of stock """
    total = db.query(models.PartInventory).count()
    out_of_stock = db.query(models.PartInventory).filter_by(
        stock_status="Out of Stock").count()

    percent_out_of_stock = (out_of_stock / total) * 100

    return f"{int(percent_out_of_stock)}% of total inventory"


@router.get("/low-stock/percent")
def low_stock_percent(db: Session = Depends(get_db)):
    """ Get percent of total inventory with low stock """
    total = db.query(models.PartInventory).count()
    low_stock = db.query(models.PartInventory).filter_by(
        stock_status="Low Stock").count()

    percent_in_stock = (low_stock / total) * 100

    return f"{int(percent_in_stock)}% of total inventory"


@router.get("/{id}")
def show(id: int, db: Session = Depends(get_db)):
    """ Get specific part """
    part = db.query(models.PartInventory).filter(
        models.PartInventory.id == id).first()

    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Part with id {id} not found")

    return part


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.PartInventory, db: Session = Depends(get_db)):
    """ Update the inventory """
    part = db.query(models.PartInventory).filter(
        models.PartInventory.id == id).update(dict(request))

    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Part with id {id} not found")

    # Update stock status ? determine_stock_status()

    db.commit()

    return "updated"


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    """ Delete a part """
    part = db.query(models.PartInventory).filter(
        models.PartInventory.id == id).delete(synchronize_session=False)

    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Part with id {id} not found")

    db.commit()
