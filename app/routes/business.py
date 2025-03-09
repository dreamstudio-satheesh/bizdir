from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Business

router = APIRouter(prefix="/business", tags=["Business"])

@router.post("/add")
def add_business(name: str, description: str, website: str, email: str, phone: str, db: Session = Depends(get_db)):
    new_business = Business(name=name, description=description, website=website, email=email, phone=phone)
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return {"message": "Business added successfully", "id": new_business.id}

@router.put("/{business_id}")
def update_business(business_id: int, name: str, description: str, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    business.name = name
    business.description = description
    db.commit()
    return {"message": "Business updated successfully"}
