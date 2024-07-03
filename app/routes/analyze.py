from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CSVData
from app.schemas import FilterModel
from typing import Dict, Any

router = APIRouter()

def add_filter_conditions(query, model, filters: Dict[str, Any]):
    for key, value in filters.items():
        column = getattr(model, key)
        if isinstance(value, str):
            query = query.filter(column.ilike(f"%{value}%"))
        else:
            query = query.filter(column == value)
    return query

@router.post("/analyze/")
async def analyze_data(
    filters: FilterModel,
    db: Session = Depends(get_db)
):
    filters_dict = filters.dict(exclude_unset=True)

    query = db.query(CSVData)
    query = add_filter_conditions(query, CSVData, filters_dict)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No matching records found.")

    # Convert comma-separated strings back to lists for Supported_languages
    for result in results:
        result.Supported_languages = result.Supported_languages.split(",")

    return results
