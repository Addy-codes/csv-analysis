import pandas as pd
import requests
from sqlalchemy.orm import Session
from app.models import CSVData
from app.schemas import CSVDataCreate
import os

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
