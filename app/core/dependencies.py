from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import EmailStr

from app.database import get_session
from app.models.user import User
from app.services import user_service
from app.core import security

# Why: OAuth2PasswordBearer is a class that provides a dependency to extract the token
# from the "Authorization: Bearer <token>" header.
# The 'tokenUrl' points to the login endpoint.
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependency to get the current user from a JWT token.
    Raises HTTPException 401 if the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email: EmailStr | None = security.decode_access_token(token)
    if not email:
        raise credentials_exception
    
    # We assume user_service will be made async. The 'await' is crucial.
    user = await user_service.get_user_by_email(session=session, email=email)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current *active* user.
    Raises HTTPException 403 if the user is marked as inactive.
    
    Why: This is a separate dependency so that we can have endpoints
    that work for inactive users if needed (e.g., an endpoint to reactivate an account).
    Most protected endpoints should depend on this one.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user
