from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class CSVData(Base):
    __tablename__ = "csv_data"

    id = Column(Integer, primary_key=True, index=True)
    AppID = Column(Integer)
    Name = Column(String)
    Release_date = Column(String)
    Required_age = Column(Integer)
    Price = Column(Float)
    DLC_count = Column(Integer)
    About_the_game = Column(String)
    Supported_languages = Column(String)
    Windows = Column(Boolean)
    Mac = Column(Boolean)
    Linux = Column(Boolean)
    Positive = Column(Integer)
    Negative = Column(Integer)
    Score_rank = Column(Integer)
    Developers = Column(String)
    Publishers = Column(String)
    Categories = Column(String)
    Genres = Column(String)
    Tags = Column(String)
