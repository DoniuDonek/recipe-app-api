"""
Test custom Django management commands
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error  #  wywala gdy nie ma db a próbujemy się połączyć

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check') #  path do pliku
class CommandTests(SimpleTestCase):
    """Test commands"""
    def test_wait_for_db_ready(self, patched_check):
        #  patched check odnosi się do argumentu patch
        """Test waiting for db if its ready """
        patched_check.return_value = True

        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep') #tylko do tego testu
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        #  im więcej testów dodamy na górze do 1 patcha, tym więcej będziemy \
        #  przepisywali tutaj
        """Test waiting for a db when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True] #za 6 razem zwróci True
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        #  jeśli nie będzie przynajmniej 6 razy, nie potrzeba używać \
        #  powyższych Exceptions
        patched_check.assert_called_with(databases=['default'])
        #  nie called_once bo będzie wywoływane wielokrotnie
