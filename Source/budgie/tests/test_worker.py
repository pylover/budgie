from budgie.worker import HelpDeskWorker
from budgie.models import AgentLog
from budgie.tests.helpers import MockupSSHTestCase


class WorkerTestCase(MockupSSHTestCase):
    """
    It's good to mock-up the ssh server for unit-testing.

    """

    def test_worker(self):
        worker = HelpDeskWorker('user1', self.mockup_server.host, port=self.mockup_server.port, key_file=self.key_file)
        worker.run()
        # worker.join()

        print(worker.result)
        self.assertDictEqual(worker.result, {
            'cpu': 40,
            'memory': 50,
        })

        log = AgentLog.query.filter(AgentLog.hostname == self.mockup_server.host).order_by(AgentLog.id.desc()).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.memory, 50)
        self.assertEqual(log.cpu, 40)
