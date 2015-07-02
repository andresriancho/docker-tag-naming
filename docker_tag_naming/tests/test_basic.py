import unittest

from docker_tag_naming.utils import get_latest_version


class BasicTest(unittest.TestCase):
    def test_has_version(self):
        version = get_latest_version('andresriancho/w3af', 'develop')
        self.assertIsInstance(version.version_number, int)
        self.assertIsInstance(version.commit, basestring)
        self.assertEqual(version.branch, 'develop')

    def test_no_version(self):
        version = get_latest_version('andresriancho/django-moth', 'develop')
        self.assertIsNone(version)

    def test_invalid_branch(self):
        version = get_latest_version('andresriancho/django-moth', 'foobar')
        self.assertIsNone(version)
