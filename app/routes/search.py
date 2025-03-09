from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from app.database import get_db
from app.models import Business, BusinessEmbedding

router = APIRouter(prefix="/search", tags=["Search"])
model = SentenceTransformer("all-MiniLM-L6-v2")

@router.get("/")
def search_business(query: str, db: Session = Depends(get_db)):
    query_vector = model.encode(query).tolist()
    businesses = db.query(Business, BusinessEmbedding).join(BusinessEmbedding, Business.id == BusinessEmbedding.business_id).all()

    scores = []
    for business, embedding in businesses:
        similarity = np.dot(query_vector, json.loads(embedding.embedding_vector))
        scores.append((business.id, business.name, business.description, similarity))

    scores.sort(key=lambda x: x[3], reverse=True)
    return {"results": [{"id": x[0], "name": x[1], "description": x[2], "score": x[3]} for x in scores[:5]]}
