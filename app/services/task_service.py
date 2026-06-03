from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime, timezone

from ..models.task import Task, TaskStatus
from ..models.user import User
from ..schemas.task import TaskCreate, TaskUpdate
from ..pagination.pagination import PaginationParams
from .notification_service import NotificationService


class TaskService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def _ensure_timezone_aware(
        self,
        dt: Optional[datetime]
    ) -> Optional[datetime]:
        """Ensure datetime is timezone-aware."""
        if dt is None:
            return None

        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)

        return dt

    def create_task(self, task_data: TaskCreate) -> Task:
        """
        Create a new task.
        """

        current_time = datetime.now(timezone.utc)

        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            scheduled_time=current_time,
            user_id=self.current_user.id
        )

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        # Schedule notifications if scheduled_time exists
        if db_task.scheduled_time:

            notification_ids = (
                NotificationService.schedule_task_notification(
                    db_task.id,
                    db_task.title,
                    self.current_user.email,
                    db_task.scheduled_time
                )
            )

            db_task.one_day_task_id = (
                notification_ids.get("one_day_task_id")
            )

            db_task.one_hour_task_id = (
                notification_ids.get("one_hour_task_id")
            )

            self.db.commit()
            self.db.refresh(db_task)

        return db_task

    def get_task(self, task_id: int) -> Task:
        """Get a single task by ID, scoped to current user."""

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
        pagination: PaginationParams,
        status: Optional[TaskStatus] = None,
        search: Optional[str] = None
    ) -> tuple[List[Task], int]:

        query = self.db.query(Task).filter(
            Task.user_id == self.current_user.id
        )

        if status:
            query = query.filter(
                Task.status == status
            )

        if search:
            query = query.filter(
                or_(
                    Task.title.ilike(
                        f"%{search}%"
                    ),
                    Task.description.ilike(
                        f"%{search}%"
                    )
                )
            )

        if (
            pagination.sort_by
            and hasattr(Task, pagination.sort_by)
        ):

            sort_column = getattr(
                Task,
                pagination.sort_by
            )

            if (
                pagination.sort_order.lower()
                == "desc"
            ):
                query = query.order_by(
                    sort_column.desc()
                )
            else:
                query = query.order_by(
                    sort_column.asc()
                )

        else:
            query = query.order_by(
                Task.created_at.desc()
            )

        total = query.count()

        tasks = (
            query
            .offset(pagination.skip)
            .limit(pagination.page_size)
            .all()
        )

        return tasks, total

    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate
    ) -> Task:
        """
        Update a task and reschedule notifications.
        """

        task = self.get_task(task_id)

        update_dict = task_data.model_dump(
            exclude_unset=True
        )

        if "scheduled_time" in update_dict:

            new_scheduled_time = (
                self._ensure_timezone_aware(
                    update_dict["scheduled_time"]
                )
            )

            update_dict[
                "scheduled_time"
            ] = new_scheduled_time

            if new_scheduled_time:

                current_time = datetime.now(
                    timezone.utc
                )

                if (
                    new_scheduled_time
                    < current_time
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            "Scheduled time "
                            "cannot be in the past"
                        )
                    )

        # Cancel existing notifications
        NotificationService.cancel_task_notifications(
            task.one_day_task_id,
            task.one_hour_task_id
        )

        for field, value in update_dict.items():
            setattr(task, field, value)

        task.one_day_task_id = None
        task.one_hour_task_id = None

        self.db.commit()
        self.db.refresh(task)

        if task.scheduled_time:

            current_time = datetime.now(
                timezone.utc
            )

            if task.scheduled_time > current_time:

                notification_ids = (
                    NotificationService.schedule_task_notification(
                        task.id,
                        task.title,
                        self.current_user.email,
                        task.scheduled_time
                    )
                )

                task.one_day_task_id = (
                    notification_ids.get(
                        "one_day_task_id"
                    )
                )

                task.one_hour_task_id = (
                    notification_ids.get(
                        "one_hour_task_id"
                    )
                )

                self.db.commit()
                self.db.refresh(task)

        return task

    def delete_task(
        self,
        task_id: int
    ) -> bool:
        """
        Delete a task and cancel reminders.
        """

        task = self.get_task(task_id)

        NotificationService.cancel_task_notifications(
            task.one_day_task_id,
            task.one_hour_task_id
        )

        self.db.delete(task)

        self.db.commit()

        return True

    def get_tasks_statistics(
        self
    ) -> dict:

        tasks = self.db.query(Task).filter(
            Task.user_id == self.current_user.id
        ).all()

        return {
            "total": len(tasks),

            "pending": sum(
                1
                for t in tasks
                if t.status == TaskStatus.PENDING
            ),

            "in_progress": sum(
                1
                for t in tasks
                if t.status == TaskStatus.IN_PROGRESS
            ),

            "completed": sum(
                1
                for t in tasks
                if t.status == TaskStatus.COMPLETED
            ),

            "scheduled": sum(
                1
                for t in tasks
                if t.scheduled_time is not None
            )
        }