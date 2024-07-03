from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import and_, or_, func

def create_csv_data(db: Session, data: schemas.CSVDataCreate):
    db_data = models.CSVData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_filtered_data(db: Session, filters: dict):
    query = db.query(models.CSVData)
    
    for field, value in filters.items():
        column = getattr(models.CSVData, field)
        
        if isinstance(value, str):
            query = query.filter(column.ilike(f"%{value}%"))
        else:
            query = query.filter(column == value)
    
    return query.all()