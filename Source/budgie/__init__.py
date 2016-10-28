
import sys

from . import cli
from .configuration import settings, init as init_config
from .server import HelpdeskObserver

__version__ = '0.1.0-dev.0'


def main():
    arguments = cli.parser.parse_args()
    if arguments.version:
        print(__version__)
        sys.exit(0)

    init_config(arguments.config_file if arguments.config_file else None)

    print(settings.clients)

