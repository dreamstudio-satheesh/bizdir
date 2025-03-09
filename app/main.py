from fastapi import FastAPI
from routers import businesses, search
from database import engine, Base

# Initialize FastAPI
app = FastAPI()

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(businesses.router, prefix="/api", tags=["Businesses"])
app.include_router(search.router, prefix="/api", tags=["Search"])

@app.get("/health")
def health_check():
    """ Health check endpoint """
    return {"status": "ok", "database": "connected"}
