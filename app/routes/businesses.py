from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Business, BusinessMeta, BusinessOwner, BusinessLocation, BusinessTag, BusinessEmbedding
from app.config import embedding_model  # Use preloaded model
from pydantic import BaseModel
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

# ✅ Business Model for Request Validation
class BusinessCreate(BaseModel):
    name: str
    description: str

# ✅ Business Meta Model
class BusinessMetaCreate(BaseModel):
    business_id: int
    meta_key: str
    meta_value: str

# ✅ Business Owner Model
class BusinessOwnerCreate(BaseModel):
    business_id: int
    owner_name: str
    contact_number: str | None = None
    email: str | None = None

# ✅ Business Location Model
class BusinessLocationCreate(BaseModel):
    business_id: int
    address: str
    city: str | None = None
    state: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None

# ✅ Business Tag Model
class BusinessTagCreate(BaseModel):
    business_id: int
    tag: str

# ✅ Vector Embedding Model
class BusinessEmbeddingCreate(BaseModel):
    business_id: int
    description: str  # Used to generate vector embeddings


@router.post("/add-business")
def add_business(business: BusinessCreate, db: Session = Depends(get_db)):
    """ Adds a business to the database """
    new_business = Business(name=business.name, description=business.description)
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return {"message": "Business added successfully", "business_id": new_business.id}


@router.post("/add-meta")
def add_business_meta(meta: BusinessMetaCreate, db: Session = Depends(get_db)):
    """ Adds metadata for a business """
    new_meta = BusinessMeta(business_id=meta.business_id, meta_key=meta.meta_key, meta_value=meta.meta_value)
    db.add(new_meta)
    db.commit()
    return {"message": "Meta data added successfully", "meta_id": new_meta.id}


@router.post("/add-owner")
def add_business_owner(owner: BusinessOwnerCreate, db: Session = Depends(get_db)):
    """ Adds an owner to a business """
    new_owner = BusinessOwner(
        business_id=owner.business_id, owner_name=owner.owner_name,
        contact_number=owner.contact_number, email=owner.email
    )
    db.add(new_owner)
    db.commit()
    return {"message": "Owner added successfully", "owner_id": new_owner.id}


@router.post("/add-location")
def add_business_location(location: BusinessLocationCreate, db: Session = Depends(get_db)):
    """ Adds a location for a business """
    new_location = BusinessLocation(
        business_id=location.business_id, address=location.address,
        city=location.city, state=location.state, country=location.country,
        latitude=location.latitude, longitude=location.longitude
    )
    db.add(new_location)
    db.commit()
    return {"message": "Location added successfully", "location_id": new_location.id}


@router.post("/add-tag")
def add_business_tag(tag: BusinessTagCreate, db: Session = Depends(get_db)):
    """ Adds a tag for a business """
    new_tag = BusinessTag(business_id=tag.business_id, tag=tag.tag)
    db.add(new_tag)
    db.commit()
    return {"message": "Tag added successfully", "tag_id": new_tag.id}


@router.post("/add-embedding")
def add_business_embedding(embedding: BusinessEmbeddingCreate, db: Session = Depends(get_db)):
    """ Generates and stores vector embeddings for a business """
    query_text = f"{embedding.description}"  # Combine name & description for better embeddings
    vector = embedding_model.encode(query_text).tolist()

    new_embedding = BusinessEmbedding(business_id=embedding.business_id, embedding_vector=json.dumps(vector))
    db.add(new_embedding)
    db.commit()
    return {"message": "Embedding added successfully", "embedding_id": new_embedding.id}



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
