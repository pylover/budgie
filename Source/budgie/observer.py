
from threading import Thread
from queue import Queue, Empty as QueueEmpty, Full as QueueFull

from budgie.configuration import settings
from budgie.worker import HelpDeskWorker


class MaximumClientsReached(Exception):
    def __init__(self, maximum):
        super(MaximumClientsReached, self).__init__('Maximum allowed %d clients is reached.' % maximum)



class HelpdeskObserver(object):
    jobs = Queue(maxsize=1000)

    def __init__(self):

        # Stacking the jobs
        try:
            for k, v in settings.clients.items():
                self.jobs.put((k, v), timeout=.1)
        except QueueFull:
            raise MaximumClientsReached(1000)

    def start(self):

        # Creating a thread-pool concept
        threads = [
            Thread(
                name='Worker: %s' % i,
                daemon=True,
                target=self.worker
            )
            for i in range(settings.workers)
        ]

        # Starting threads
        for thread in threads:
            thread.start()

        # Waiting
        for thread in threads:
            thread.join()

    def worker(self):
        while True:
            try:
                name, config = self.jobs.get(timeout=.1)
            except QueueEmpty:
                break

            agent = HelpDeskWorker(
                config.username,
                config.hostname,
                port=config.port,
                key_file=config.key_file,
                password=None if not hasattr(config, 'password') else config.password
            )

            agent.run()

            # Check for alerts
            agent.check_for_alerts(config.alerts, config.mail)

