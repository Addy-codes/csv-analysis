import os
import requests
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CSVData
from app.utils import(
    get_csv_export_link,
    download_csv,
    save_csv_to_db,
    UPLOAD_DIR
)

router = APIRouter()

@router.post("/upload/")
async def upload_csv(file_url: str, db: Session = Depends(get_db)):
    try:
        export_link = get_csv_export_link(file_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    file_name = "exported_data.csv"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    try:
        download_csv(export_link, file_path)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to download CSV file: {str(e)}")
    
    try:
        db.query(CSVData).delete()
        db.commit()
        save_csv_to_db(file_path, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save CSV data to database: {str(e)}")
    
    return {"filename": file_name}
