from datetime import datetime, timedelta, timezone
import logging

from celery.result import AsyncResult

from app.workers.notification_tasks import (
    send_notification
)

logger = logging.getLogger(__name__)


class NotificationService:

    @classmethod
    def schedule_task_notification(
        cls,
        task_id: int,
        task_title: str,
        user_email: str,
        scheduled_time: datetime
    ):
        if scheduled_time.tzinfo is None:
            scheduled_time = scheduled_time.replace(
                tzinfo=timezone.utc
            )

        now = datetime.now(timezone.utc)

        result = {
            "one_day_task_id": None,
            "one_hour_task_id": None
        }

        one_day_before = (
            scheduled_time - timedelta(days=1)
        )

        if one_day_before > now:

            task = send_notification.apply_async(
                args=[
                    task_id,
                    task_title,
                    user_email,
                    "1 day"
                ],
                eta=one_day_before
            )

            result["one_day_task_id"] = task.id

            logger.info(
                f"1-day reminder scheduled "
                f"for task {task_id}"
            )

        one_hour_before = (
            scheduled_time - timedelta(hours=1)
        )

        if one_hour_before > now:

            task = send_notification.apply_async(
                args=[
                    task_id,
                    task_title,
                    user_email,
                    "1 hour"
                ],
                eta=one_hour_before
            )

            result["one_hour_task_id"] = task.id

            logger.info(
                f"1-hour reminder scheduled "
                f"for task {task_id}"
            )

        return result

    @classmethod
    def cancel_task_notifications(
        cls,
        one_day_task_id=None,
        one_hour_task_id=None
    ):
        for task_id in [
            one_day_task_id,
            one_hour_task_id
        ]:
            if task_id:
                AsyncResult(task_id).revoke(
                    terminate=False
                )