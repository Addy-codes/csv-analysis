import pandas as pd
import requests
from sqlalchemy.orm import Session
from app import crud, schemas

def download_csv(url: str, file_path: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        f.write(response.content)

def save_csv_to_db(file_path: str, db: Session):
    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        csv_data = schemas.CSVDataCreate(**row.to_dict())
        crud.create_csv_data(db, csv_data)
