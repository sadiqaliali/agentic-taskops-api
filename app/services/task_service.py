from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.task import Task, TaskCreate, TaskUpdate
from app.models.user import User

async def create_task_for_user(
    session: AsyncSession, *, task_in: TaskCreate, owner: User
) -> Task:
    """
    Creates a new task owned by a specific user.

    Args:
        session: The database session.
        task_in: The task creation data.
        owner: The user who will own the task.

    Returns:
        The newly created task object.
    """
    # Why: We manually construct the Task object, ensuring all required fields
    # including the owner_id are explicitly set from trusted sources.
    # This prevents validation errors and correctly associates the task with its owner.
    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        owner_id=owner.id  # Explicitly set owner_id from the authenticated user
    )
    
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

async def get_tasks_for_user(
    session: AsyncSession, *, owner: User, skip: int = 0, limit: int = 100
) -> List[Task]:
    """
    Retrieves a list of tasks for a specific user with pagination.

    Args:
        session: The database session.
        owner: The user whose tasks to retrieve.
        skip: The number of tasks to skip.
        limit: The maximum number of tasks to return.

    Returns:
        A list of task objects.
    """
    statement = select(Task).where(Task.owner_id == owner.id).offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()

async def get_task_for_user(
    session: AsyncSession, *, task_id: int, owner: User
) -> Task:
    """
    Retrieves a single task by its ID, ensuring it belongs to the specified owner.

    Args:
        session: The database session.
        task_id: The ID of the task to retrieve.
        owner: The user who should own the task.

    Returns:
        The task object if found and owned by the user.
        
    Raises:
        HTTPException: If the task is not found or not owned by the user.
    """
    statement = select(Task).where(Task.id == task_id, Task.owner_id == owner.id)
    result = await session.exec(statement)
    task = result.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

async def update_task_for_user(
    session: AsyncSession, *, task_id: int, task_update: TaskUpdate, owner: User
) -> Task:
    """

    Updates a task, ensuring the user performing the update is the owner.

    Args:
        session: The database session.
        task_id: The ID of the task to update.
        task_update: The data to update the task with.
        owner: The user performing the update.

    Returns:
        The updated task object.

    Raises:
        HTTPException: If the task is not found or not owned by the user.
    """
    db_task = await get_task_for_user(session=session, task_id=task_id, owner=owner)
    
    # Why: Using model_dump with exclude_unset=True ensures we only get the data
    # that was explicitly provided in the PATCH request.
    update_data = task_update.model_dump(exclude_unset=True)
    
    # Why: Iterating and setting attributes individually is a more robust and
    # explicit way to apply updates than the deprecated sqlmodel_update method.
    # This prevents unexpected behavior and ensures only the intended fields are changed.
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

async def delete_task_for_user(session: AsyncSession, *, task_id: int, owner: User):
    """
    Deletes a task, ensuring the user performing the action is the owner.

    Args:
        session: The database session.
        task_id: The ID of the task to delete.
        owner: The user performing the deletion.

    Raises:
        HTTPException: If the task is not found or not owned by the user.
    """
    task = await get_task_for_user(session=session, task_id=task_id, owner=owner)
    
    await session.delete(task)
    await session.commit()
    return {"ok": True}
