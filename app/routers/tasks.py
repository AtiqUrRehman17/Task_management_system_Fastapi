from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..models.user import User
from ..models.task import TaskStatus
from ..schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse
)
from ..schemas.common import ResponseModel
from ..services.task_service import TaskService
from ..pagination.pagination import PaginationParams

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=ResponseModel[TaskResponse])
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task. Scheduled time is auto-set to current UTC time."""
    task_service = TaskService(db, current_user)
    task = task_service.create_task(task_data)

    return ResponseModel(
        success=True,
        message="Task created successfully",
        data=TaskResponse.model_validate(task)
    )


@router.get("/", response_model=ResponseModel[TaskListResponse])
def get_tasks(
    pagination: PaginationParams = Depends(),
    status: Optional[TaskStatus] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all tasks for the current user with pagination and filtering."""
    task_service = TaskService(db, current_user)

    # No apply_pagination() call here — service handles pagination internally
    tasks, total = task_service.get_tasks(
        pagination=pagination,
        status=status,
        search=search
    )

    return ResponseModel(
        success=True,
        message="Tasks retrieved successfully",
        data=TaskListResponse(
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            tasks=[
                TaskResponse.model_validate(task)
                for task in tasks
            ]
        )
    )


@router.get("/statistics/summary", response_model=ResponseModel[dict])
def get_task_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get task statistics for the current user."""
    task_service = TaskService(db, current_user)
    stats = task_service.get_tasks_statistics()

    return ResponseModel(
        success=True,
        message="Statistics retrieved successfully",
        data=stats
    )


@router.get("/{task_id}", response_model=ResponseModel[TaskResponse])
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific task by ID."""
    task_service = TaskService(db, current_user)
    task = task_service.get_task(task_id)

    return ResponseModel(
        success=True,
        message="Task retrieved successfully",
        data=TaskResponse.model_validate(task)
    )


@router.put("/{task_id}", response_model=ResponseModel[TaskResponse])
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a task."""
    task_service = TaskService(db, current_user)
    task = task_service.update_task(task_id, task_data)

    return ResponseModel(
        success=True,
        message="Task updated successfully",
        data=TaskResponse.model_validate(task)
    )


@router.delete("/{task_id}", response_model=ResponseModel[bool])
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a task."""
    task_service = TaskService(db, current_user)
    task_service.delete_task(task_id)

    return ResponseModel(
        success=True,
        message="Task deleted successfully",
        data=True
    )