from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

"""
    helper command: it will ensure that the database is up and ready
    to accept connections before we try and access database
    patch: mock the behavior of the Django get database function.
    simulate database is being available and not being available
    call_command: call the command in our source code
    OperationalError: Django throws when database is unavailable.
     simulate database is being available and not being,
      available when we run our command
"""


class CommandTests(TestCase):
    """What happens when we call our command and database is
    already available"""
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # side effect to the function that we are,
            # mocking (function: __getitem__)
            # raise OperationalError 5 times
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
