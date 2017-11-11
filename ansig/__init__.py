from argparse import ArgumentParser
from os import environ
from sys import stdout

from ansig.generator import Generator

__version__ = '0.3.0'


def load(filename=None):
    ''' Dynamic inventory generator loader function '''

    parser = ArgumentParser(
        version=u'%(prog)s ' + __version__,
        description=u'Dynamic inventory generator for Ansible.')
    parser.add_argument(
        '--list', action='store_true', dest='list',
        help='generates a list of available hosts and their metadata')
    parser.add_argument(
        '--host', action='store', dest='host',
        help='generates all the metadata for a specific host')
    parser.add_argument(
        '--refresh', action='store_true', dest='refresh',
        help='disable caching')
    parser.add_argument(
        '--debug', action='store_true', dest='debug',
        default=environ.get('ANSIG_DEBUG', False),
        help='enable debugging')
    parser.add_argument(
        '--log', action='store', dest='log',
        default=environ.get('ANSIG_LOG'),
        help='log debugging information to file')
    args = parser.parse_args()

    # Create generator object
    generator = Generator(filename)

    # Generate debugging information
    if args.debug or args.log:
        log = open(args.log, 'w') if args.log else stdout
        log.write(generator.generate_debug_info())

    # Generate output data
    if args.list:
        stdout.write(generator.generate_host_list(args.refresh))
    elif args.host:
        stdout.write(generator.generate_host_info(args.host, args.refresh))
