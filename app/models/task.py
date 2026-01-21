from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship

# Forward reference to avoid circular imports
# from .user import User, UserRead

# --- Task Schemas ---

class TaskStatus(str, Enum):
    """
    Enum for the status of a task to ensure data consistency.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

# Why: The base model contains shared properties.
class TaskBase(SQLModel):
    title: str = Field(index=True, description="The title of the task.")
    description: Optional[str] = Field(default=None, description="A detailed description of the task.")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="The current status of the task.")

# Why: The table model represents the 'task' table in the database.
# It includes the foreign key to the user table.
class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Why: Foreign key relationship to the 'user' table.
    # This ensures that every task is owned by a user.
    # 'nullable=False' makes this a required relationship at the database level.
    owner_id: int = Field(foreign_key="user.id", nullable=False)

    # Why: Defines the many-to-one relationship.
    # Many tasks can belong to one owner. 'back_populates' links this to the
    # 'tasks' field in the 'User' model.
    owner: "User" = Relationship(back_populates="tasks")

# --- API-Facing Schemas ---

# Why: This model is used when creating a new task.
# It defines the data a client must provide. The owner_id is not included here
# because it will be derived from the authenticated user's token.
class TaskCreate(TaskBase):
    pass

# Why: This model is for updating an existing task.
# All fields are optional, so a client can update just one piece of information.
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

# Why: This is the default model for reading/returning task data.
# It provides a clean representation of the task itself.
class TaskRead(TaskBase):
    id: int
    owner_id: int

# Why: A more detailed model that includes the task's owner information.
# This is useful for endpoints where the client needs to know who owns the task.
# It uses the 'UserRead' schema to avoid exposing sensitive user data.
class TaskReadWithUser(TaskRead):
    owner: "UserRead"
