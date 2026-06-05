from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from ..models.task import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    scheduled_time: Optional[datetime] = None

    @field_validator('scheduled_time')
    def validate_scheduled_time(cls, v):
        if v is None or v == "":
            return None

        # If it's a string, try to parse it
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v.replace('Z', '+00:00'))
            except:
                raise ValueError('Invalid datetime format. Use ISO format like "2024-12-25T10:00:00Z"')

        # Make timezone-aware if naive
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)

        return v


class TaskResponse(TaskBase):
    id: int
    user_id: int
    scheduled_time: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    tasks: list[TaskResponse]


class TaskStatisticsResponse(BaseModel):
    total: int
    pending: int
    in_progress: int
    completed: int
    scheduled: int