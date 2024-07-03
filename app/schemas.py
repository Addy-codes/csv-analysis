from pydantic import BaseModel
from typing import Optional, List

class CSVDataCreate(BaseModel):
    AppID: int
    Name: str
    Release_date: str
    Required_age: int
    Price: float
    DLC_count: int
    About_the_game: str
    Supported_languages: List[str]
    Windows: bool
    Mac: bool
    Linux: bool
    Positive: int
    Negative: int
    Score_rank: Optional[int]
    Developers: str
    Publishers: str
    Categories: str
    Genres: str
    Tags: str

class FilterModel(BaseModel):
    AppID: Optional[int] = None
    Name: Optional[str] = None
    Release_date: Optional[str] = None
    Required_age: Optional[int] = None
    Price: Optional[float] = None
    DLC_count: Optional[int] = None
    About_the_game: Optional[str] = None
    Supported_languages: Optional[str] = None
    Windows: Optional[bool] = None
    Mac: Optional[bool] = None
    Linux: Optional[bool] = None
    Positive: Optional[int] = None
    Negative: Optional[int] = None
    Score_rank: Optional[int] = None
    Developers: Optional[str] = None
    Publishers: Optional[str] = None
    Categories: Optional[str] = None
    Genres: Optional[str] = None
    Tags: Optional[str] = None