from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User, UserCreate

async def get_user_by_email(session: AsyncSession, email: EmailStr) -> User | None:
    """
    Retrieves a user by their email address from the database.

    Args:
        session: The database session.
        email: The email address to search for.

    Returns:
        The User object if found, otherwise None.
    """
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalars().first()


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    """
    Creates a new user in the database.

    Args:
        session: The database session.
        user_in: The user creation data.

    Returns:
        The newly created user object.
        
    Raises:
        HTTPException: If a user with the same email already exists.
    """
    # Why: First, check if a user with this email already exists to prevent duplicates.
    existing_user = await get_user_by_email(session, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    # Why: Hash the password before storing it. Never store plain text passwords.
    hashed_password = get_password_hash(user_in.password)

    # Why: Create a User model instance from the input data.
    # We explicitly exclude the plain password and set the hashed_password.
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password
        # is_active defaults to True as defined in the model
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user
