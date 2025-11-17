"""Management command to check environment configuration."""

from django.core.management.base import BaseCommand

from api.utils import validate_environment


class Command(BaseCommand):
    """Check if all required environment variables are configured."""

    help = "Check if all required environment variables are configured"

    def handle(self, *args, **options):
        """Execute the command."""
        is_valid, missing, warnings = validate_environment()

        if missing:
            self.stdout.write(
                self.style.ERROR("❌ Missing required environment variables:")
            )
            for var in missing:
                self.stdout.write(self.style.ERROR(f"  - {var}"))

        if warnings:
            self.stdout.write(
                self.style.WARNING("\n⚠️  Optional environment variables not set:")
            )
            for var in warnings:
                self.stdout.write(self.style.WARNING(f"  - {var}"))

        if is_valid and not warnings:
            self.stdout.write(
                self.style.SUCCESS("\n✅ All environment variables are configured!")
            )
        elif is_valid:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✅ All required environment variables are configured!"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    "   Some optional features may not work without the optional variables."
                )
            )
