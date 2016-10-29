
import sys

from . import cli
from .configuration import settings, init as init_config
from .observer import HelpdeskObserver
from .models import init as init_models, metadata, engine

__version__ = '0.1.0-dev.0'


def start_server(cli_arguments):
    init_models()
    observer = HelpdeskObserver()
    observer.start()

def main():
    arguments = cli.init()
    if arguments.version:
        print(__version__)
        sys.exit(0)

    init_config(arguments.config_file if arguments.config_file else None)

    if arguments.func is not None:
        arguments.func(arguments)


