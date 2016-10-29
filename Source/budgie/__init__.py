
import sys

from sqlalchemy.exc import DatabaseError

from . import cli
from .configuration import settings, init as init_config
from .observer import HelpdeskObserver, MaximumClientsReached
from .models import init as init_models, metadata, engine, check_db
from .smtp import SMTPConfigurationError


__version__ = '0.1.0-dev.0'


def start_server(cli_arguments):
    init_models()

    # Checking database
    try:
        check_db()
    except DatabaseError:
        print(
            'Cannot connect to database. or database objects are not created yet. Please run `budgie setup-db`.',
            file=sys.stderr
        )
        sys.exit(-1)


    try:
        manager = HelpdeskObserver()
        manager.start()
    except (
            MaximumClientsReached,
            SMTPConfigurationError) as ex:
        print(ex, file=sys.stderr)
        sys.exit(-1)


def main():
    arguments = cli.init()
    if arguments.version:
        print(__version__)
        sys.exit(0)

    init_config(arguments.config_file if arguments.config_file else None)

    if arguments.func is not None:
        arguments.func(arguments)


