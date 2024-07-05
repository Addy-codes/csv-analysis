import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    UPLOAD_DIR: str = os.environ.get("UPLOAD_DIR","data")
    SECRET_KEY: str = os.environ.get("SECRET_KEY","7eF9$zG#T@y2^W!x5Q$r3%v8*b6&uD+p")
    ALGORITHM: str = os.environ.get("ALGORITHM","HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)