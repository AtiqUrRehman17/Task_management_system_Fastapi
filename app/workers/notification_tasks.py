import logging

from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def send_notification(
    self,
    task_id: int,
    task_title: str,
    user_email: str,
    when: str
):
    notification_message = f"""
    REMINDER:
    Task "{task_title}" (ID: {task_id})
    is due in {when}.
    """

    logger.info(
        f"Notification sent to {user_email}: "
        f"{notification_message}"
    )

    return {
        "task_id": task_id,
        "email": user_email,
        "when": when
    }