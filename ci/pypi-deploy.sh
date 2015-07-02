#!/bin/bash

set -e

echo "[server-login]" > ~/.pypirc
echo "username:" $PYPI_USER >> ~/.pypirc
echo "password:" $PYPI_PASSWORD >> ~/.pypirc

PACKAGE_URL='https://pypi.python.org/packages/source/d/docker-tag-naming/'

packages=`curl -f -s -S -k $PACKAGE_URL`
dtn_version=`python -c 'from docker_tag_naming import __VERSION__;print __VERSION__,'`
current_package="docker-tag-naming-${dtn_version}.tar.gz"

if [[ $packages == *$current_package* ]]
then
    echo "Current package version is already at PyPi. If your intention was to"
    echo " release a new version, you'll have to increase the version number."
else
    echo "Uploading $dtn_version version to PyPi"
    python setup.py sdist upload
fi