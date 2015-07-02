from __future__ import print_function

import sys
import time

from docker_tag_naming.utils import get_latest_version, DockerTagNamingException


def run_refresh(args):
    """
    Handle the refresh subcommand
    :param args: Parsed command line arguments
    :return: None, output is written to console
    """
    image = args.image
    branch = args.branch

    try:
        initial_version = get_latest_version(image, branch)
    except DockerTagNamingException, de:
        print(de)
        sys.exit(1)

    if initial_version is None:
        print('No version found')
        sys.exit(1)

    print('Initial version is %s , waiting for new release...' % initial_version)

    for _ in xrange(120):
        time.sleep(1)

        try:
            version = get_latest_version(image, branch)
        except DockerTagNamingException, de:
            print(de)
            sys.exit(1)

        if version.version_number != initial_version.version_number:
            print('New version found: %s' % version)
            sys.exit(0)

    print('Timeout: version did not change.')
    sys.exit(0)

