import argparse

from .bump import run_bump
from .latest import run_latest
from .forge import run_forge


def parse_args_and_run():
    """
    :return: The parsed arguments
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Docker-tag-naming sub-commands')

    parser_forge = subparsers.add_parser('forge',
                                         help='Create a new version tag')
    parser_forge.add_argument('--version', type=int, default=1,
                              help='Version number')
    parser_forge.add_argument('--commit-id', required=True,
                              help='Git commit id')
    parser_forge.add_argument('--branch', required=True,
                              help='The branch name (ie. master)')
    parser_forge.set_defaults(func=run_forge)

    parser_latest = subparsers.add_parser('latest',
                                          help='Query the latest tag in the'
                                               ' registry')
    parser_latest.add_argument('image', nargs='+',
                               help='The image to query (ie. username/image)')
    parser_latest.add_argument('branch', nargs='+',
                               help='The branch name (ie. master)')
    parser_latest.set_defaults(func=run_latest)

    parser_bump = subparsers.add_parser('bump',
                                        help='Query the latest tag in the'
                                             ' registry and return a +1')
    parser_bump.add_argument('image', nargs='+',
                             help='The image to bump (ie. username/image)')
    parser_bump.add_argument('branch', nargs='+',
                             help='The branch name (ie. master)')
    parser_bump.add_argument('--commit-id', required=True,
                             help='Git commit id for the newly created tag')
    parser_latest.set_defaults(func=run_bump)

    args = parser.parse_args()
    args.func(args)


def main():
    """
    Main entry point for the docker-tag-naming command, parse command line
    arguments, call functions and output the data.

    :return: Exit code
    """
    parse_args_and_run()
