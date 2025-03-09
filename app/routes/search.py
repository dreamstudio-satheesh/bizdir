from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Business, BusinessEmbedding, BusinessLocation, BusinessTag
from config import embedding_model  # Use preloaded model
import numpy as np
import json

router = APIRouter()

@router.get("/search")
def search_businesses(
    query: str,
    location: str = Query(None),  # Optional location filter
    tag: str = Query(None),       # Optional tag filter
    db: Session = Depends(get_db)
):
    """ Search businesses using vector embeddings with optional filters """

    # Generate vector embeddings from the query
    query_vector = embedding_model.encode(query).tolist()

    # Fetch all businesses that have embeddings
    embedding_query = db.query(BusinessEmbedding)

    # Apply location filter if provided
    if location:
        embedding_query = embedding_query.join(BusinessLocation).filter(BusinessLocation.city == location)

    # Apply tag filter if provided
    if tag:
        embedding_query = embedding_query.join(BusinessTag).filter(BusinessTag.tag.ilike(f"%{tag}%"))

    businesses_with_embeddings = embedding_query.all()

    if not businesses_with_embeddings:
        raise HTTPException(status_code=404, detail="No businesses found matching the criteria.")

    # Compute similarity scores
    scores = []
    for business in businesses_with_embeddings:
        similarity_score = np.dot(query_vector, json.loads(business.embedding_vector))
        scores.append((business.business_id, similarity_score))

    # Sort results by highest similarity
    scores.sort(key=lambda x: x[1], reverse=True)

    # Fetch detailed business info
    results = []
    for business_id, score in scores[:5]:  # Return top 5 results
        business = db.query(Business).filter(Business.id == business_id).first()
        if business:
            results.append({
                "id": business.id,
                "name": business.name,
                "description": business.description,
                "score": score,
                "location": db.query(BusinessLocation).filter(BusinessLocation.business_id == business.id).first(),
                "tags": [t.tag for t in db.query(BusinessTag).filter(BusinessTag.business_id == business.id).all()]
            })

    return {"results": results}
