from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Business, BusinessEmbedding
from app.config import embedding_model  # Use preloaded model
import numpy as np
import json

router = APIRouter()

@router.get("/search")
def search_businesses(query: str, db: Session = Depends(get_db)):
    """ Search businesses using vector embeddings """
    query_vector = embedding_model.encode(query).tolist()

    businesses = db.query(BusinessEmbedding).all()
    if not businesses:
        raise HTTPException(status_code=404, detail="No businesses found")

    scores = []
    for business in businesses:
        similarity_score = np.dot(query_vector, json.loads(business.embedding_vector))
        scores.append((business.business_id, similarity_score))

    scores.sort(key=lambda x: x[1], reverse=True)

    results = []
    for business_id, score in scores[:5]:  # Return top 5 results
        business = db.query(Business).filter(Business.id == business_id).first()
        if business:
            results.append({"id": business.id, "name": business.name, "description": business.description, "score": score})

    return {"results": results}
