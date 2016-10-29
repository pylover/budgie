

from os.path import abspath, dirname, join, exists
import os
import unittest

import mockssh

from budgie.configuration import init as init_config, settings
from budgie.models import init as init_models, metadata, engine


THIS_DIR = abspath(dirname(__file__))
TEST_STUFF_DIR = join(THIS_DIR, 'stuff')


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        db_file = join(THIS_DIR, 'data', 'test_%s.db' % self.__class__.__name__.lower())
        if exists(db_file):
            os.remove(db_file)

        init_config(context=dict(here=THIS_DIR, db_file=db_file), force=True)
        settings.merge("""
        db:
          uri: sqlite:///%(db_file)s

        agent:
          filename: %(here)s/client/budgie_agent.py
        """)

        init_models()
        metadata.create_all(engine, checkfirst=True)


class MockupSSHTestCase(DatabaseTestCase):

    def setUp(self):
        super(MockupSSHTestCase, self).setUp()
        self.ssh_users = {
            "user1": join(TEST_STUFF_DIR, 'user1.key')
        }
        self.key_file = join(TEST_STUFF_DIR, 'user1.key')
        self.mockup_server = mockssh.Server(self.ssh_users)
        self.mockup_server.__enter__()

    def tearDown(self):
        self.mockup_server.__exit__()