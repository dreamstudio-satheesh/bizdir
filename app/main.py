from fastapi import FastAPI, HTTPException
import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import uvicorn

# Initialize FastAPI
app = FastAPI()

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Database connection details
DB_CONFIG = {
    "dbname": "business_directory",
    "user": "postgres",
    "password": "strongpassword",
    "host": "postgres",  # Docker service name (not localhost)
    "port": "5432",
}

# Initialize database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

@app.on_event("startup")
def startup_event():
    global db, cursor
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        print("✅ Connected to PostgreSQL")
    else:
        print("❌ Failed to connect to PostgreSQL")

@app.on_event("shutdown")
def shutdown_event():
    if db:
        db.close()
        print("✅ Database connection closed")

@app.get("/health")
def health_check():
    """ Health check endpoint to verify API status """
    return {"status": "ok"}

@app.get("/search")
def search_businesses(query: str):
    """ Search businesses using vector embeddings """
    try:
        logging.info(f"🔍 Searching for: {query}")

        db = get_db_connection()
        if not db:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = db.cursor()

        query_vector = model.encode(query).tolist()

        # Fetch embeddings from business_embeddings & join with businesses
        cursor.execute("""
            SELECT b.id, b.name, b.description, be.embedding_vector 
            FROM business_embeddings be
            JOIN businesses b ON be.business_id = b.id
        """)
        
        results = cursor.fetchall()

        # Compute similarity
        scores = []
        for row in results:
            try:
                similarity_score = np.dot(query_vector, json.loads(row[3]))  # Compute cosine similarity
                scores.append((row[0], row[1], row[2], similarity_score))
            except Exception as e:
                logging.error(f"⚠️ Error processing row {row[0]}: {e}")

        # Sort results by highest similarity
        scores.sort(key=lambda x: x[3], reverse=True)

        return {"results": [{"id": x[0], "name": x[1], "description": x[2], "score": x[3]} for x in scores[:5]]}

    except Exception as e:
        logging.error(f"❌ Error in /search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
