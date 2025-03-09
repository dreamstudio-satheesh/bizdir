from fastapi import FastAPI, HTTPException
import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Load the text embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# PostgreSQL connection settings
DB_CONFIG = {
    "dbname": "business_directory",
    "user": "postgres",
    "password": "strongpassword",
    "host": "postgres",  # Docker service name
    "port": "5432",
}

# Initialize database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logging.error(f"❌ Database connection failed: {e}")
        return None
