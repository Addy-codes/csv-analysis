from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas import TokenData, UserCreate
from app.models import User as DBUser
from app.database import get_db
from app.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    """
    Hashes a given plain text password.

    Args:
        password: The plain text password to hash.

    Returns:
        The hashed password as a string.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain text password against a hashed password.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to verify against.

    Returns:
        True if the password is valid, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token with an optional expiration time.

    Args:
        data: The data to encode in the token.
        expires_delta: The time delta after which the token will expire. If None, defaults to 15 minutes.

    Returns:
        The encoded JWT as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def get_user(db: Session, email: str):
    """
    Retrieves a user from the database by email or username.

    Args:
        db: The SQLAlchemy database session.
        email: The email or username of the user to retrieve.

    Returns:
        The user object if found, otherwise None.
    """
    return db.query(DBUser).filter(DBUser.email == email).first() or db.query(DBUser).filter(DBUser.username == email).first()

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticates a user by verifying their password.

    Args:
        db: The SQLAlchemy database session.
        email: The email or username of the user to authenticate.
        password: The plain text password to verify.

    Returns:
        The user object if authentication is successful, otherwise False.
    """
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieves the current user based on the provided JWT token.

    Args:
        token: The JWT token from the request.
        db: The SQLAlchemy database session.

    Returns:
        The user object if authentication is successful.

    Raises:
        HTTPException: If the token is invalid or the user cannot be authenticated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            print("email is none")
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        print("JWTError")
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        print("User is none")
        raise credentials_exception
    return user

def create_user(db: Session, user: UserCreate):
    """
    Creates a new user in the database.

    Args:
        db: The SQLAlchemy database session.
        user: The user data to create, including username, email, and password.

    Returns:
        The created user object.
    """
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
