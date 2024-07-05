import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth_utils import get_current_user
from app.models import CSVData, User as DBUser
from app.utils import(
    get_csv_export_link,
    download_csv,
    save_csv_to_db,
)
from app.config import Config

router = APIRouter()

@router.post("/upload/")
async def upload_csv(file_url: str, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    """
    Uploads a CSV file from a provided URL and saves its data to the database.

    Args:
        file_url: The URL of the CSV file to upload.
        db: The SQLAlchemy database session.
        current_user: The currently authenticated user.

    Returns:
        A dictionary containing the name of the uploaded file.

    Raises:
        HTTPException: If the file URL is invalid, downloading the CSV file fails,
                       or saving the CSV data to the database fails.
    """
    try:
        export_link = get_csv_export_link(file_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    file_name = "exported_data.csv"
    file_path = os.path.join(Config.UPLOAD_DIR, file_name)
    
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
