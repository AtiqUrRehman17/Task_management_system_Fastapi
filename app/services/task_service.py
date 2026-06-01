from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime, timezone
from ..models.task import Task, TaskStatus
from ..models.user import User
from ..schemas.task import TaskCreate, TaskUpdate
from .notification_service import NotificationService

class TaskService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user
    
    def _ensure_timezone_aware(self, dt: Optional[datetime]) -> Optional[datetime]:
        """Ensure datetime is timezone-aware"""
        if dt is None:
            return None
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    
    def create_task(self, task_data: TaskCreate) -> Task:
        # Automatically set scheduled_time to current UTC time
        current_time = datetime.now(timezone.utc)
        
        # Create task with automatic scheduled_time
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            scheduled_time=current_time,  # Auto-set to current time
            user_id=self.current_user.id
        )
        
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        return db_task
    
    def get_task(self, task_id: int) -> Task:
        task = self.db.query(Task).filter(
            and_(
                Task.id == task_id,
                Task.user_id == self.current_user.id
            )
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return task
    
    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[TaskStatus] = None,
        search: Optional[str] = None
    ) -> tuple[List[Task], int]:
        query = self.db.query(Task).filter(Task.user_id == self.current_user.id)
        
        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        
        if search:
            query = query.filter(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%")
                )
            )
        
        # Order by created_at descending (newest first)
        query = query.order_by(Task.created_at.desc())
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        tasks = query.offset(skip).limit(limit).all()
        
        return tasks, total
    
    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        
        # Track if scheduled time changed
        old_scheduled_time = self._ensure_timezone_aware(task.scheduled_time)
        update_dict = task_data.model_dump(exclude_unset=True)
        
        # Handle scheduled_time if present in update
        if 'scheduled_time' in update_dict:
            new_scheduled_time = self._ensure_timezone_aware(update_dict['scheduled_time'])
            update_dict['scheduled_time'] = new_scheduled_time
            
            # Validate if scheduled_time is not in the past (only if being updated)
            if new_scheduled_time:
                current_time = datetime.now(timezone.utc)
                if new_scheduled_time < current_time:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Scheduled time cannot be in the past"
                    )
        
        # Update fields
        for field, value in update_dict.items():
            setattr(task, field, value)
        
        self.db.commit()
        self.db.refresh(task)
        
        # Handle notification rescheduling if needed
        if 'scheduled_time' in update_dict:
            new_scheduled_time = self._ensure_timezone_aware(task.scheduled_time)
            # Cancel old notifications
            NotificationService.cancel_task_notifications(task_id)
            # Schedule new notifications if applicable and if it's a future time
            if new_scheduled_time:
                current_time = datetime.now(timezone.utc)
                if new_scheduled_time > current_time:
                    NotificationService.schedule_task_notification(
                        task.id,
                        task.title,
                        self.current_user.email,
                        new_scheduled_time
                    )
        
        return task
    
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        
        # Cancel scheduled notifications
        NotificationService.cancel_task_notifications(task_id)
        
        self.db.delete(task)
        self.db.commit()
        
        return True
    
    def get_tasks_statistics(self) -> dict:
        tasks = self.db.query(Task).filter(Task.user_id == self.current_user.id).all()
        
        stats = {
            "total": len(tasks),
            "pending": sum(1 for t in tasks if t.status == TaskStatus.PENDING),
            "in_progress": sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS),
            "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            "scheduled": sum(1 for t in tasks if t.scheduled_time is not None)
        }
        
        return stats