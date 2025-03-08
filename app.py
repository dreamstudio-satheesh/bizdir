from fastapi import FastAPI, Query
import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
import json

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

db = psycopg2.connect("dbname=business_directory user=postgres password=strongpassword host=postgres")
cursor = db.cursor()

@app.get("/search")
def search_businesses(query: str):
    query_vector = model.encode(query).tolist()
    
    # Search in PostgreSQL (pgvector)
    cursor.execute("SELECT id, name, description, embedding_vector FROM business_embeddings")
    results = cursor.fetchall()

    # Compute similarity
    scores = [(row[0], row[1], row[2], np.dot(query_vector, json.loads(row[3]))) for row in results]
    scores.sort(key=lambda x: x[3], reverse=True)

    return {"results": [{"id": x[0], "name": x[1], "description": x[2], "score": x[3]} for x in scores[:5]]}
