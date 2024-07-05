from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, User, Token
from datetime import timedelta
from app.auth_utils import (
    authenticate_user,
    create_access_token,
    create_user,
    get_user
    )
from app.config import Config

router = APIRouter()

@router.post("/register/", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in the database.

    Args:
        user: The user data to create, including username, email, and password.
        db: The SQLAlchemy database session.

    Returns:
        The created user object.

    Raises:
        HTTPException: If the email is already registered.
    """
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT access token.

    Args:
        form_data: The form data containing username and password.
        db: The SQLAlchemy database session.

    Returns:
        A token object containing the access token and token type.

    Raises:
        HTTPException: If the email or password is incorrect.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    print(access_token)
    return Token(access_token= access_token, token_type= "bearer")