import requests
import logging

from requests.exceptions import RequestException
from .constants import VERSION_FORMAT

API_URL = 'https://registry.hub.docker.com/v1/repositories/%s'


class Version(object):
    def __init__(self, version_number, commit, branch):
        self.version_number = version_number
        self.commit = commit
        self.branch = branch

    def __str__(self):
        return VERSION_FORMAT % (self.version_number, self.commit, self.branch)

    def bump(self):
        self.version_number += 1


def version_parser(version_string):
    """
    :param version_string: The version tag as returned by the registry/hub API
    :return: A tuple with the parsed version / an exception when the version
             format is unknown/incorrect
    """
    version, commit, branch = version_string.split('-', 3)

    # Remove the "v"
    version_number = version[1:]
    version_number = int(version_number)

    return Version(version_number, commit, branch)


def get_all_tags(image_name, branch=None):
    """
    GET /v1/repositories/<namespace>/<repository_name>/tags

    :param image_name: The docker image name
    :param branch: The branch to filter by
    :return: A list of Version instances, latest first
    """
    output = []

    spec = '%s/tags' % image_name
    try:
        response = requests.get(API_URL % spec)
    except RequestException, re:
        raise DockerTagNamingException('HTTP request exception "%s"' % re)

    if response.status_code != 200:
        msg = ('Received unexpected status code %s from the registry'
               ' REST API, the image might not exist or is private.')
        raise DockerTagNamingException(msg % response.status_code)

    try:
        json_data = response.json()
    except ValueError:
        msg = 'JSON decode failed! Raw data is: "%s". Please report a bug.'
        raise DockerTagNamingException(msg % (response.content[:25]).strip())

    try:
        tag_names = [tag_info['name'] for tag_info in json_data]
    except Exception:
        msg = ('The JSON data does not contain the expected format!'
               ' Raw data is: "%s". Please report a bug.')
        raise DockerTagNamingException(msg % (response.content[:25]).strip())

    for tag_name in tag_names:

        try:
            version = version_parser(tag_name)
        except Exception, e:
            msg = 'Ignoring version tag "%s" with incorrect format: "%s"'
            logging.debug(msg % (tag_name, e))
            continue

        if branch is not None:
            if version.branch != branch:
                continue

        output.append(version)

    def sort_func(version_a, version_b):
        return cmp(version_b.version_number, version_a.version_number)

    output.sort(sort_func)

    return output


def get_latest_version(image_name, branch):
    all_tags = get_all_tags(image_name, branch=branch)
    if all_tags:
        return all_tags[0]
    return None


def version_bump(image_name, branch, commit):
    version = get_latest_version(image_name, branch)
    if version is None:
        return Version(1, commit, branch)

    version.bump()
    version.commit = commit
    return version


class DockerTagNamingException(Exception):
    pass