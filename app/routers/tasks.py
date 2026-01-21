from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.task import TaskCreate, TaskRead, TaskUpdate
from app.models.user import User
from app.services import task_service
from app.core.dependencies import get_current_active_user

# Why: Grouping this router's endpoints under a "Tasks" tag in the API docs.
router = APIRouter(tags=["Tasks"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskRead)
async def create_task(
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    task_in: TaskCreate,
) -> TaskRead:
    """
    Create a new task for the current authenticated user.
    """
    task = await task_service.create_task_for_user(
        session=session, task_in=task_in, owner=current_user
    )
    return task

@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> List[TaskRead]:
    """
    Retrieve all tasks for the current authenticated user.
    """
    tasks = await task_service.get_tasks_for_user(
        session=session, owner=current_user, skip=skip, limit=limit
    )
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def read_task(
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    task_id: int,
) -> TaskRead:
    """
    Retrieve a specific task by its ID.
    The service layer ensures the task belongs to the current user.
    """
    task = await task_service.get_task_for_user(
        session=session, task_id=task_id, owner=current_user
    )
    return task

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    task_id: int,
    task_update: TaskUpdate,
) -> TaskRead:
    """
    Update a task.
    The service layer ensures the task belongs to the current user.
    """
    task = await task_service.update_task_for_user(
        session=session, task_id=task_id, task_update=task_update, owner=current_user
    )
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    *,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    task_id: int,
):
    """
    Delete a task.
    The service layer ensures the task belongs to the current user.
    """
    await task_service.delete_task_for_user(
        session=session, task_id=task_id, owner=current_user
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
