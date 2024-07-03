import os
import requests
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CSVData
from app.schemas import CSVDataCreate

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def download_csv(file_url: str, file_path: str):
    response = requests.get(file_url)
    response.raise_for_status()
    with open(file_path, 'wb') as f:
        f.write(response.content)

def save_csv_to_db(file_path: str, db: Session):
    data = pd.read_csv(file_path)
    
    for index, row in data.iterrows():
        csv_data = CSVData(
            AppID=row['AppID'],
            Name=row['Name'],
            Release_date=row['Release date'],
            Required_age=row['Required age'],
            Price=row['Price'],
            DLC_count=row['DLC count'],
            About_the_game=row['About the game'],
            Supported_languages=",".join(eval(row['Supported languages'])),  # Convert list to comma-separated string
            Windows=row['Windows'],
            Mac=row['Mac'],
            Linux=row['Linux'],
            Positive=row['Positive'],
            Negative=row['Negative'],
            Score_rank=row['Score rank'],
            Developers=row['Developers'],
            Publishers=row['Publishers'],
            Categories=row['Categories'],
            Genres=row['Genres'],
            Tags=row.get('Tags', '')
        )
        db.add(csv_data)
    db.commit()

def get_csv_export_link(google_sheets_url: str) -> str:
    if 'docs.google.com/spreadsheets' not in google_sheets_url:
        raise ValueError("Invalid Google Sheets URL.")
    file_id = google_sheets_url.split('/d/')[1].split('/')[0]
    export_link = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    return export_link

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
        save_csv_to_db(file_path, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save CSV data to database: {str(e)}")
    
    return {"filename": file_name}
