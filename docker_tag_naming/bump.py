from __future__ import print_function

import sys

from docker_tag_naming.utils import version_bump, DockerTagNamingException


def run_bump(args):
    """
    Handle the bump subcommand
    :param args: Parsed command line arguments
    :return: None, output is written to console
    """
    commit_id = args.commit_id
    image = args.image
    branch = args.branch

    try:
        print(version_bump(image, branch, commit_id))
    except DockerTagNamingException, de:
        print(de)
        sys.exit(1)