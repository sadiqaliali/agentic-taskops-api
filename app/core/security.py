from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from config.settings import settings

# --- Password Hashing ---

# Why: Use passlib's CryptContext for password hashing.
# 'bcrypt' is the chosen scheme for its strength and resistance to brute-force attacks.
# 'deprecated="auto"' ensures that older hashes (if any other schemes were used) can still be validated.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against its hashed version.

    Args:
        plain_password: The password as entered by the user.
        hashed_password: The hashed password stored in the database.

    Returns:
        True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generates a hashed version of a plain text password.

    Args:
        password: The plain text password to hash.

    Returns:
        The resulting hashed password.
    """
    # Why: The bcrypt algorithm has a maximum password length of 72 bytes.
    # Passlib's bcrypt handler will raise a ValueError if the password is too long.
    # To prevent this, we encode the password to bytes and truncate it to 72
    # before hashing. This is the standard way to handle this limitation.
    password_bytes = password.encode('utf-8')
    truncated_password_bytes = password_bytes[:72]
    return pwd_context.hash(truncated_password_bytes)


# --- JWT Token Schemas & Functions ---

class Token(BaseModel):
    """Schema for the JWT access token returned on successful login."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for the data encoded within the JWT (the 'subject')."""
    email: Optional[EmailStr] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.

    Args:
        data: The data to be encoded in the token (e.g., user email).
        expires_delta: Optional timedelta to override the default expiration.

    Returns:
        The encoded JWT as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[EmailStr]:
    """
    Decodes a JWT access token to extract the user's email.

    Args:
        token: The JWT token string.

    Returns:
        The user's email if the token is valid, otherwise None.
        In a real application, this would raise specific exceptions.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: Optional[EmailStr] = payload.get("sub")
        if email is None:
            return None
        # Here you could load the user from DB and attach to the request
        return email
    except JWTError:
        # This catches any error from jose (e.g., expired token, invalid signature)
        return None
