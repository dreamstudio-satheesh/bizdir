from fastapi import FastAPI
from app.routes import business, search

app = FastAPI()

app.include_router(business.router)
app.include_router(search.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
