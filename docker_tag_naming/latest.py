from __future__ import print_function

import sys

from docker_tag_naming.utils import get_latest_version, DockerTagNamingException


def run_latest(args):
    """
    Handle the latest subcommand
    :param args: Parsed command line arguments
    :return: None, output is written to console
    """
    image = args.image
    branch = args.branch

    try:
        version = get_latest_version(image, branch)
    except DockerTagNamingException, de:
        print(de)
        sys.exit(1)

    if version is None:
        sys.exit(1)

    print(version)

