from fastapi import FastAPI
from app.routes import upload, analyze
from app.database import engine, Base

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(upload.router)
app.include_router(analyze.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the CSV Analysis API"}
