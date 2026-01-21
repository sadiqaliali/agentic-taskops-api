from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import create_access_token, verify_password, Token
from app.database import get_session
from app.models.user import UserCreate, UserRead
from app.services import user_service
from config.settings import settings

# Why: Grouping this router's endpoints under an "Authentication" tag in the API docs.
router = APIRouter(tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(
    user_in: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    """
    Register a new user.
    The service layer handles the check for existing users.
    """
    # Why: The business logic (checking for existing user, hashing password)
    # is encapsulated in the service layer. The router's job is to handle
    # the HTTP request/response and call the appropriate service.
    user = await user_service.create_user(session=session, user_in=user_in)
    return UserRead.from_orm(user)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate a user and return a JWT access token.
    
    Why: Uses OAuth2PasswordRequestForm for standard username/password login flow.
    The 'username' field is used for the email.
    """

    user = await user_service.get_user_by_email(session=session, email=form_data.username)
    
    # Why: We check if the user exists AND if the provided password is correct.
    # It's crucial to use the verified security function for this.
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Why: Create a token with the user's email as the subject ('sub').
    # This subject is what our 'get_current_user' dependency will decode.
    access_token = create_access_token(data={"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer")
