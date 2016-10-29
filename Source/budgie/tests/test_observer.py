
from budgie.observer import HelpdeskObserver
from budgie.configuration import settings
from budgie.tests.helpers import MockupSSHTestCase, mockup_smtp_server


class ObserverTestCase(MockupSSHTestCase):

    def setUp(self):
        super(ObserverTestCase, self).setUp()
        settings.merge("""
        workers: 1

        smtp:
          startls: false
          auth: false
          host: localhost
          port: 2526
          local_hostname: localhost

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
        with mockup_smtp_server(2526):
            observer = HelpdeskObserver()
            observer.start()






