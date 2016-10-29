

from os.path import abspath, dirname, join, exists
import socket
import os
import unittest
import smtpd
import asyncore
import contextlib
import threading
import mockssh
import time

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
        print('Starting mocked-up SSH server.')
        self.mockup_server.__enter__()

    def tearDown(self):
        print('Shutting down mocked-up SSH server.')
        self.mockup_server.__exit__()
        try:
            self.mockup_server._socket.shutdown(socket.SHUT_RDWR)
            self.mockup_server._socket.close()
            print('Waiting for SSH thread to stop.')
            self.mockup_server._thread.join()
        except Exception:
            pass
        finally:
            self.mockup_server._socket = None
            self.mockup_server._thread = None
            time.sleep(.2)


class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(self, port, **kwargs):
        print("Running fake smtp server on port 25")
        super(FakeSMTPServer, self).__init__(('localhost', port), None, **kwargs)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def process_message(*args, **kwargs):
        pass


@contextlib.contextmanager
def mockup_smtp_server(port):
    server = FakeSMTPServer(port)
    smtp_thread = threading.Thread(daemon=True, target=asyncore.loop)
    print('Starting mocked-up SMTP server.')
    smtp_thread.start()
    yield server
    print('Shutting down mocked-up SMTP server.')
    server.close()
    print('Waiting for SMTP thread to stop.')
    smtp_thread.join(timeout=.5)
