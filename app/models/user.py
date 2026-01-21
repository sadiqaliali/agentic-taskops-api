from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship

# Forward reference to avoid circular imports
# from .task import Task, TaskRead
# We use strings "Task" and "TaskRead" to tell SQLModel/Pydantic about the types
# without actually importing them, which would cause a circular dependency.

# --- User Schemas ---

# Why: The base model contains shared properties.
# Other models inherit from it to avoid code duplication.
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, description="User's unique email address.")
    is_active: bool = Field(default=True, description="Flag to indicate if the user account is active.")

# Why: The table model represents the 'user' table in the database.
# It includes fields that should not be exposed in API responses, like hashed_password.
# The 'table=True' argument marks this as a database table model.
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(description="The salted and hashed password for the user.")

    # Why: Defines the one-to-many relationship.
    # A single user can have multiple tasks. 'back_populates' links this to the
    # 'owner' field in the 'Task' model, creating a bidirectional relationship.
    tasks: List["Task"] = Relationship(back_populates="owner")


# --- API-Facing Schemas ---

# Why: This model is used for creating a new user (e.g., during registration).
# It inherits from UserBase and adds the 'password' field, which is required for creation.
# This password will be hashed before being stored in the database.
class UserCreate(SQLModel):
    email: EmailStr
    password: str

# Why: This model is used for reading/returning user data from the API.
# It explicitly includes only the fields that are safe to expose to clients.
# Crucially, it omits 'hashed_password'.
class UserRead(UserBase):
    id: int

# Why: A more detailed model for reading a user along with their associated tasks.
# This demonstrates how to create different "views" of your data for different API endpoints.
class UserReadWithTasks(UserRead):
    tasks: List["TaskRead"] = []

# Why: This model is for updating a user. All fields are optional,
# allowing clients to update only the fields they need to change.
class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
