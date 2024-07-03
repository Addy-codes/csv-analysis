# create_tables.py

from app.database import Base, engine
from app.models import CSVData

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")
