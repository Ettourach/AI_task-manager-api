from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def process_due_reminders():
    """
    Process all due reminders that haven't been sent yet.
    This task is scheduled to run every minute via Celery Beat.
    """
    from .models import Reminder
    
    now = timezone.now()
    due_reminders = Reminder.objects.filter(
        remind_at__lte=now,
        sent=False
    ).select_related('task', 'created_by')

    processed_count = 0
    for reminder in due_reminders:
        try:
            # In a real application, you would send an email or push notification
            # For now, we just mark the reminder as sent
            # Example email sending (requires email configuration):
            # send_mail(
            #     subject=f'Reminder: {reminder.task.title}',
            #     message=f'This is a reminder for your task: {reminder.task.title}',
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[reminder.created_by.email],
            #     fail_silently=True,
            # )
            
            reminder.sent = True
            reminder.save()
            processed_count += 1
        except Exception as e:
            # Log the error but continue processing other reminders
            print(f"Error processing reminder {reminder.id}: {e}")
    
    return f"Processed {processed_count} reminders"


@shared_task
def send_reminder_notification(reminder_id):
    """
    Send a notification for a specific reminder.
    """
    from .models import Reminder
    
    try:
        reminder = Reminder.objects.select_related('task', 'created_by').get(id=reminder_id)
        if not reminder.sent:
            # Send notification logic here
            reminder.sent = True
            reminder.save()
            return f"Sent notification for reminder {reminder_id}"
    except Reminder.DoesNotExist:
        return f"Reminder {reminder_id} not found"
    
    return f"Reminder {reminder_id} already sent"
