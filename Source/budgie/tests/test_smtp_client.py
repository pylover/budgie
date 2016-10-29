

import unittest

from budgie.smtp import SMTPClient
from budgie.tests.helpers import mockup_smtp_server
from budgie.configuration import init as init_config, settings


class SMTPClientTestCase(unittest.TestCase):

    def setUp(self):
        init_config(force=True)
        settings.merge("""
        smtp:
          host: localhost
          port: 2525
          local_hostname: localhost

        """)

    def test_client(self):
        with mockup_smtp_server() as smtp_server, SMTPClient(auth=False) as smtp_client:

            smtp_client.send(
                "vahid@crossover.com",
                "admin@crossover.com",
                "Test email",
                "Something good was happening!"
            )
