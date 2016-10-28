
import sys
import argparse

DEFAULT_CONFIG_FILE='development.yaml'
DEFAULT_WORKERS = 10

# CLI Arguments
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('-c', '--config-file', default=DEFAULT_CONFIG_FILE,
                    help='The server configuration file, default: %s' % DEFAULT_CONFIG_FILE)
parser.add_argument('-V', '--version', action='store_true', help='Show the version.')


