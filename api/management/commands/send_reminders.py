"""
Management command to process and send due reminders.
Usage: python manage.py send_reminders
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Reminder


class Command(BaseCommand):
    help = 'Process and send all due reminders that have not been sent yet'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually sending reminders',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()
        
        due_reminders = Reminder.objects.filter(
            remind_at__lte=now,
            sent=False
        ).select_related('task', 'created_by')

        reminder_count = due_reminders.count()
        
        if reminder_count == 0:
            self.stdout.write(self.style.SUCCESS('No due reminders to process.'))
            return

        self.stdout.write(f'Found {reminder_count} due reminder(s).')

        if dry_run:
            for reminder in due_reminders:
                self.stdout.write(
                    f'  [DRY RUN] Would send reminder for task: "{reminder.task.title}" '
                    f'to user: {reminder.created_by.username}'
                )
            return

        processed_count = 0
        error_count = 0

        for reminder in due_reminders:
            try:
                # In a real application, you would send an email or push notification here
                # For example:
                # send_mail(
                #     subject=f'Reminder: {reminder.task.title}',
                #     message=f'This is a reminder for your task: {reminder.task.title}',
                #     from_email=settings.DEFAULT_FROM_EMAIL,
                #     recipient_list=[reminder.created_by.email],
                # )
                
                reminder.sent = True
                reminder.save()
                processed_count += 1
                self.stdout.write(
                    f'  Sent reminder for task: "{reminder.task.title}" '
                    f'to user: {reminder.created_by.username}'
                )
            except Exception as e:
                error_count += 1
                self.stderr.write(
                    self.style.ERROR(f'  Error processing reminder {reminder.id}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Processed {processed_count} reminder(s) successfully. '
                f'{error_count} error(s).'
            )
        )
