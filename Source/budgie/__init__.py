
import sys

from . import cli
from .configuration import settings, init as init_config
from .observer import HelpdeskObserver
from .models import init as init_models, metadata, engine

__version__ = '0.1.0-dev.0'


def start_server(cli_arguments):
    print('START SERVER')


def main():
    arguments = cli.init()
    if arguments.version:
        print(__version__)
        sys.exit(0)

    init_config(arguments.config_file if arguments.config_file else None)

    print(arguments.func)
    if arguments.func is not None:
        arguments.func(arguments)


