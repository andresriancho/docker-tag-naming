Motivation
==========

When building complex docker ecosystems it's important to uniquely tag each
docker build before pushing it to the registry. This allows you to move back
and forward in time by using different versions of the docker image, pin
the production/QA/staging environments to different tags, etc.

Installation
============

::

    $ pip install --upgrade docker-tag-naming


Commands
========

One of the most interesting features which comes with using `docker-tag-naming`
is that it's now possible to query which tag is the latest in a specific branch:

::

    $ docker-tag-naming latest andresriancho/w3af develop
    v112-01460cd-develop

According to our convention `112` is the version number, `01460cd` is the `git`
commit ID and `develop` is the branch.

It's possible to manually forge a new version tag to be used in any registry
image:

::

    $ docker-tag-naming forge --version 332 --commit-id cd14580 --branch master
    v332-cd14580-master

But the most interesting feature is to `bump` the version:

::

    $ docker-tag-naming bump andresriancho/w3af develop --commit-id cd14580
    v113-cd14580-develop

Please note that `113` was created by retrieving the latest version tag from the
`andresriancho/w3af` repository and performing a `+1`.


Continuous delivery usage
=========================

These are just a couple of examples to show how to use `docker-tag-naming` with
continuous delivery. First in the base image use `bump` to tag and push the
version:

::

    $ export NEXT_TAG=`docker-tag-naming bump username/base-image ${BRANCH} --commit-id ${COMMIT_ID}`
    $ docker tag username/base-image username/base-image:$NEXT_TAG
    $ docker push username/base-image:$NEXT_TAG

Then in the build where the base image is used, query the latest:

::

    $ export LATEST_TAG=`docker-tag-naming latest username/base-image develop`
    $ render-compose --latest-base-image $LATEST_TAG
    $ docker-compose up

Using these steps will guarantee that the latest available image is always used
in your builds.

Important disclaimer
====================

The docker registry/hub (https://registry.hub.docker.com/) seems to have a delay
between what's shown through the web interface (your browser) and the REST API.
Take this into account when using these commands in continuous integration
scripts, since your recently pushed tags might not appear right away!

A command that might help as a workaround is `docker-tag-naming refresh` which
will query the API until a new version is available or the timeout is reached:

::

    $ docker-tag-naming refresh username/base-image develop
    Initial version is v113-cd14580-develop , waiting for new release...
    New version found: v114-5151bc0-develop

    $ docker-tag-naming latest andresriancho/w3af develop
    v114-5151bc0-develop


Reporting bugs
==============

Report your issues and feature requests in `docker-tag-naming's issue
tracker <https://github.com/andresriancho/docker-tag-naming>`_ and we'll
be more than glad to fix them.

Pull requests are more than welcome!

Build status
============

.. image:: https://circleci.com/gh/andresriancho/docker-tag-naming.svg?style=svg
    :target: https://circleci.com/gh/andresriancho/docker-tag-naming

