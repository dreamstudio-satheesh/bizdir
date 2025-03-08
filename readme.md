# Business Directory with PostgreSQL & Faiss

## Overview
This project is a **scalable business directory** that leverages **PostgreSQL (pgvector)** and **Faiss** for efficient similarity search. The system supports tagging-based classification, AI-powered search, and optimized database storage for large datasets.

## Features
- **AI-powered search** with vector embeddings.
- **Hybrid search** using SQL filtering and Faiss ranking.
- **Flexible tagging system** instead of rigid categories.
- **Multi-location support** for businesses.
- **Efficient storage** using PostgreSQL and pgvector.

---

## System Architecture
1. **PostgreSQL (pgvector)** stores **business metadata + embeddings**.
2. **Faiss** is used for **fast approximate nearest neighbor (ANN) search**.
3. **Hybrid Search:** SQL filtering first, followed by Faiss ranking for the best results.

---

## Installation & Setup

### Prerequisites
- **Python 3.8+**
- **PostgreSQL 14+** (with `pgvector` extension)
- **pip**

### Step 1: Install PostgreSQL & pgvector
```bash
# Install PostgreSQL
sudo apt update && sudo apt install postgresql -y

# Install pgvector extension
psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Step 2: Install Required Python Libraries
```bash
pip install psycopg2 faiss-cpu sentence-transformers pgvector tqdm
```
_For GPU acceleration, use:_
```bash
pip install faiss-gpu
```

---

## Database Schema

### Core Tables
- **businesses** → Stores general business details.
- **business_meta** → Stores additional attributes as key-value pairs.
- **business_tags** → Supports flexible tagging.
- **business_owners** → Stores owner details.
- **business_locations** → Allows multiple locations per business.
- **business_embeddings** → Stores AI-based vector representations.

Example Table for Vector Storage:
```sql
CREATE TABLE business_embeddings (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    embedding_vector JSON NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);
```

---

## Generating & Storing Business Embeddings
```python
import psycopg2
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to PostgreSQL
db = psycopg2.connect(dbname="business_directory", user="postgres", password="your_password")
cursor = db.cursor()

# Example data
businesses = [
    ("DreamCoderZ", "Software development specializing in AI."),
    ("GreenMart", "Organic store with home delivery.")
]

# Insert business embeddings
for name, description in businesses:
    embedding = model.encode(description).tolist()
    cursor.execute(
        "INSERT INTO businesses (name, description) VALUES (%s, %s) RETURNING id",
        (name, description)
    )
    business_id = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO business_embeddings (business_id, embedding_vector) VALUES (%s, %s)",
        (business_id, embedding)
    )

db.commit()
print("✅ Businesses inserted successfully.")
```

---

## Future Enhancements
- Implement a **REST API** using FastAPI or Flask.
- Deploy a **real-time update system** with background Faiss indexing.
- Optimize search performance with **HNSW indexing in Faiss**.

---

## Contributing
Feel free to submit issues, suggestions, or pull requests to enhance the project!

🚀 **Happy coding!**

