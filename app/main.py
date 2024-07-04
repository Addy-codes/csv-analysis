from fastapi import FastAPI
from app.routes import upload, analyze, auth
from app.database import engine, Base
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuth2 as OAuth2Model


app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    

# Include routers
app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(auth.router)



@app.get("/")
def read_root():
    return {"message": "Welcome to the CSV Analysis API"}
