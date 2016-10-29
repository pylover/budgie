
from budgie.observer import HelpdeskObserver
from budgie.configuration import settings
from budgie.tests.helpers import MockupSSHTestCase


class UbserverTestCase(MockupSSHTestCase):

    def setUp(self):
        super(UbserverTestCase, self).setUp()
        settings.merge("""
        workers: 2
        clients:
          localhost:
            mail: admin@localhost.com
            hostname: %s
            port: %s
            username: 'user1'
            key_file: %s
            alerts:
              -
                type: memory
                limit: 50
              -
                type: cpu
                limit: 20
        """ % (
            self.mockup_server.host,
            self.mockup_server.port,
            self.key_file,
        ))

    def test_observer(self):
        observer = HelpdeskObserver()
        observer.start()






