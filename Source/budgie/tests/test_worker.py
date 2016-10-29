
from os.path import abspath, dirname, join, exists
import os
import unittest

import mockssh

from budgie.configuration import init as init_config, settings
from budgie.worker import HelpDeskWorker
from budgie.models import AgentLog, init as init_models, metadata, engine


THIS_DIR = abspath(dirname(__file__))
TEST_STUFF_DIR = join(THIS_DIR, 'stuff')


class WorkerTestCase(unittest.TestCase):
    """
    It's good to mock-up the ssh server for unit-testing.


    """

    def setUp(self):
        db_file = join(THIS_DIR, 'data', 'test_worker.db')
        if exists(db_file):
            os.remove(db_file)

        init_config(context=dict(here=THIS_DIR, db_file=db_file))
        settings.merge("""
        db:
          uri: sqlite:///%(db_file)s
        """)

        init_models()
        metadata.create_all(engine, checkfirst=True)

        self.ssh_users = {
            "user1": join(TEST_STUFF_DIR, 'user1.key')
        }

    def test_worker(self):
        with mockssh.Server(self.ssh_users) as s:

            key_file = join(TEST_STUFF_DIR, 'user1.key')
            worker = HelpDeskWorker('user1', s.host, port=s.port, key_file=key_file)
            worker.start()
            worker.join()

            print(worker.result)
            self.assertDictEqual(worker.result, {
                'cpu': 40,
                'memory': 50,
            })

            log = AgentLog.query.filter(AgentLog.hostname == s.host).order_by(AgentLog.id.desc()).first()
            self.assertIsNotNone(log)
            self.assertEqual(log.memory, 50)
            self.assertEqual(log.cpu, 40)
