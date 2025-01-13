"""
Django command to wait for the database to become available
"""
import time
from psycopg import OperationalError as PsycopgError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                db_conn = connections['default']
                c = db_conn.cursor()
                db_up = True
            except (PsycopgError, OperationalError):
                self.stdout.write(f'Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))