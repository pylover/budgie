
import sys
import argparse


DEFAULT_CONFIG_FILE='development.yaml'
DEFAULT_WORKERS = 10


def init():
    """
    Initialize the CLI Arguments

    :return: The parsed CLI arguments.
    """

    from budgie import start_server
    from budgie.models import create_database_objects

    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-c', '--config-file', default=DEFAULT_CONFIG_FILE,
                        help='The server configuration file, default: %s' % DEFAULT_CONFIG_FILE)
    parser.add_argument('-V', '--version', action='store_true', help='Show the version.')

    sub_parser = parser.add_subparsers(help='Available commands:')

    # Adding the command setup-db, to make the database objects
    setup_db_parser = sub_parser.add_parser('setup-db')
    setup_db_parser.set_defaults(func=create_database_objects)

    # Adding the run command, the main entry point of the server app.
    run_parser = sub_parser.add_parser('run')
    run_parser.set_defaults(func=start_server)

    return parser.parse_args()
