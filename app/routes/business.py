from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Business
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

@router.post("/add-business")
def add_business(name: str, description: str, db: Session = Depends(get_db)):
    """ Adds a business to the database """
    new_business = Business(name=name, description=description)
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return {"message": "Business added successfully", "business_id": new_business.id}

@router.put("/{business_id}")
def update_business(business_id: int, name: str = None, description: str = None, db: Session = Depends(get_db)):
    """ Updates business details """
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    if name:
        business.name = name
    if description:
        business.description = description

    db.commit()
    return {"message": f"Business {business_id} updated successfully"}
