"""
  Django command to wait for db to be available
"""
import time
from psycopg2 import OperationalError as Psycopg20pError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """  Django command to wait for db  """
    def handle(self, *args, **options):
        """  Entrypoint for command  """
        self.stdout.write('Waiting for database...')   #  zwraca info
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True   #  jeśli True to zwraca sukces z dołu self.stdout
            except (Psycopg20pError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 sec..')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Db available!'))

