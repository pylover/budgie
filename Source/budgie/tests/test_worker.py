
from os.path import abspath, dirname, join
import unittest

import mockssh
import paramiko


from budgie.configuration import settings


THIS_DIR = abspath(dirname(__file__))
TEST_STUFF_DIR = join(THIS_DIR, 'stuffs')


class WorkerTestCase(unittest.TestCase):
    """
    It;s good to mock-up the ssh server for unit-testing.


    """

    def setUp(self):
        self.ssh_users = {
            "user1": join(TEST_STUFF_DIR, 'user1.key')
        }


    def test_worker(self):
        with mockssh.Server(self.ssh_users) as s:



