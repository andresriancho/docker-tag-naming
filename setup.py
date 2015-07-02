#!/usr/bin/env python
import os

from setuptools import setup, find_packages
from os.path import join, dirname
from docker_tag_naming import __VERSION__


if os.environ.get('CIRCLECI', None) is not None:
    # monkey-patch distutils upload
    #
    # http://bugs.python.org/issue21722
    # https://github.com/tagcubeio/tagcube-cli/issues/4
    try:
        from distutils.command import upload as old_upload_module
        from ci.upload import upload as fixed_upload
        old_upload_module.upload = fixed_upload
    except ImportError:
        # In some cases I install tagcube-cli in CircleCI, but not from the
        # repository where the ci module is present
        pass


setup(
    name='docker-tag-naming',

    version=__VERSION__,
    license='GNU General Public License v2 (GPLv2)',
    platforms='Linux',

    description='Name and query docker tags',
    long_description=file(join(dirname(__file__), 'README.rst')).read(),

    author='Andres Riancho',
    author_email='andres.riancho@gmail.com',
    url='https://github.com/andresriancho/docker-tag-naming/',

    packages=find_packages(exclude=('ci',)),
    include_package_data=True,
    install_requires=['requests[security]>=2.7.0'],

    entry_points = {
        'console_scripts': [
            'docker-tag-naming = docker_tag_naming.main:main',
        ],
    },

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Monitoring'
    ],

    # In order to run this command: python setup.py test
    test_suite="nose.collector",
    tests_require="nose",
)

