import argparse

from .bump import run_bump
from .latest import run_latest
from .forge import run_forge


def parse_args_and_run():
    """
    :return: The parsed arguments
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Docker-tag-naming sub-commands',
                                       dest='subparser_name')

    #
    #   Forge
    #
    parser_forge = subparsers.add_parser('forge',
                                         help='Create a new version tag')
    parser_forge.add_argument('--version', type=int, default=1,
                              help='Version number')
    parser_forge.add_argument('--commit-id', required=True,
                              help='Git commit id')
    parser_forge.add_argument('--branch', required=True,
                              help='The branch name (ie. master)')

    #
    #   Latest
    #
    parser_latest = subparsers.add_parser('latest',
                                          help='Query the latest tag in the'
                                               ' registry')
    parser_latest.add_argument('image',
                               help='The image to query (ie. username/image)')
    parser_latest.add_argument('branch',
                               help='The branch name (ie. master)')

    #
    #   Bump
    #
    parser_bump = subparsers.add_parser('bump',
                                        help='Query the latest tag in the'
                                             ' registry and return a +1')
    parser_bump.add_argument('image',
                             help='The image to bump (ie. username/image)')
    parser_bump.add_argument('branch',
                             help='The branch name (ie. master)')
    parser_bump.add_argument('--commit-id', required=True,
                             help='Git commit id for the newly created tag')

    args = parser.parse_args()
    
    {'bump': run_bump,
     'latest': run_latest,
     'forge': run_forge}.get(args.subparser_name)(args)


def main():
    """
    Main entry point for the docker-tag-naming command, parse command line
    arguments, call functions and output the data.

    :return: Exit code
    """
    parse_args_and_run()
