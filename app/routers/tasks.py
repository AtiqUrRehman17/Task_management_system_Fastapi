from fastapi import APIRouter, Depends
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
from ..services.task_service import TaskService
from ..pagination.pagination import PaginationParams
from ..utils.response import api_response

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task. Scheduled time is auto-set to current UTC time."""
    task_service = TaskService(db, current_user)
    task = task_service.create_task(task_data)

    return api_response(
        status=True,
        message="Task created successfully",
        data=TaskResponse.model_validate(task).model_dump()
    )


@router.get("/")
def get_tasks(
    pagination: PaginationParams = Depends(),
    status: Optional[TaskStatus] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all tasks for the current user with pagination and filtering."""
    task_service = TaskService(db, current_user)

    tasks, total = task_service.get_tasks(
        pagination=pagination,
        status=status,
        search=search
    )

    response_data = TaskListResponse(
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        tasks=[
            TaskResponse.model_validate(task)
            for task in tasks
        ]
    )

    return api_response(
        status=True,
        message="Tasks retrieved successfully",
        data=response_data.model_dump()
    )


@router.get("/statistics/summary")
def get_task_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get task statistics for the current user."""
    task_service = TaskService(db, current_user)
    stats = task_service.get_tasks_statistics()

    return api_response(
        status=True,
        message="Statistics retrieved successfully",
        data=stats
    )


@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific task by ID."""
    task_service = TaskService(db, current_user)
    task = task_service.get_task(task_id)

    return api_response(
        status=True,
        message="Task retrieved successfully",
        data=TaskResponse.model_validate(task).model_dump()
    )


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a task."""
    task_service = TaskService(db, current_user)
    task = task_service.update_task(task_id, task_data)

    return api_response(
        status=True,
        message="Task updated successfully",
        data=TaskResponse.model_validate(task).model_dump()
    )


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a task."""
    task_service = TaskService(db, current_user)
    task_service.delete_task(task_id)

    return api_response(
        status=True,
        message="Task deleted successfully",
        data=True
    )