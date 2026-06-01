from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta, timezone
from typing import Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    _scheduler = None
    
    @classmethod
    def get_scheduler(cls):
        if cls._scheduler is None:
            cls._scheduler = BackgroundScheduler(timezone='UTC')
            cls._scheduler.start()
        return cls._scheduler
    
    @classmethod
    def schedule_task_notification(cls, task_id: int, task_title: str, user_email: str, scheduled_time: datetime):
        scheduler = cls.get_scheduler()
        
        # Ensure scheduled_time is timezone-aware
        if scheduled_time.tzinfo is None:
            scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        
        # Schedule notification 1 hour before
        one_hour_before = scheduled_time - timedelta(hours=1)
        if one_hour_before > now:
            scheduler.add_job(
                cls._send_notification,
                trigger=DateTrigger(run_date=one_hour_before),
                args=[task_id, task_title, user_email, "1 hour"],
                id=f"task_{task_id}_1hour",
                replace_existing=True
            )
            logger.info(f"Scheduled 1-hour notification for task {task_id} at {one_hour_before}")
        
        # Schedule notification 1 day before
        one_day_before = scheduled_time - timedelta(days=1)
        if one_day_before > now:
            scheduler.add_job(
                cls._send_notification,
                trigger=DateTrigger(run_date=one_day_before),
                args=[task_id, task_title, user_email, "1 day"],
                id=f"task_{task_id}_1day",
                replace_existing=True
            )
            logger.info(f"Scheduled 1-day notification for task {task_id} at {one_day_before}")
    
    @classmethod
    def _send_notification(cls, task_id: int, task_title: str, user_email: str, when: str):
        notification_message = f"""
        REMINDER: Task "{task_title}" (ID: {task_id}) is due in {when}!
        Please check your task management system for details.
        """
        logger.info(f"Notification sent to {user_email}: {notification_message}")
        # Here you would typically send an actual email or push notification
        
    @classmethod
    def cancel_task_notifications(cls, task_id: int):
        scheduler = cls.get_scheduler()
        job_ids = [f"task_{task_id}_1hour", f"task_{task_id}_1day"]
        for job_id in job_ids:
            try:
                scheduler.remove_job(job_id)
                logger.info(f"Cancelled notification {job_id} for task {task_id}")
            except:
                pass