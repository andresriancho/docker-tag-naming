from __future__ import print_function

import sys

from docker_tag_naming.utils import Version, DockerTagNamingException


def run_forge(args):
    """
    Handle the forge subcommand
    :param args: Parsed command line arguments
    :return: None, output is written to console
    """
    version = args.version
    commit_id = args.commit_id
    branch = args.branch

    try:
        print(Version(version, commit_id, branch))
    except DockerTagNamingException, de:
        print(de)
        sys.exit(1)

