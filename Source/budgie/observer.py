
import functools
from threading import Thread
from queue import Queue, Empty as QueueEmpty

from budgie.configuration import settings
from budgie.worker import HelpDeskWorker


def worker(jobs_stack):

    while True:
        try:
            name, config = jobs_stack.get(timeout=.1)
        except QueueEmpty:
            break

        HelpDeskWorker(
            config.username,
            config.hostname,
            port=config.port,
            key_file=config.key_file,
            password=None if not hasattr(config, 'password') else config.password
        ).run()


class HelpdeskObserver(object):
    jobs = Queue(maxsize=1000)

    def __init__(self):

        # Stacking the jobs
        for k, v in settings.clients.items():
            self.jobs.put((k, v))

    def start(self):

        # Creating a thread-pool concept
        threads = [
            Thread(name='Worker: %s' % i, target=functools.partial(worker, self.jobs))
            for i in range(settings.workers)
        ]

        # Starting threads
        for thread in threads:
            thread.start()

        # Waiting
        for thread in threads:
            thread.join()
