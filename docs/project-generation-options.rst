Project Generation Options
==========================

project_name:
    Your project's human-readable name, capitals and spaces allowed.

project_slug:
    Your project's slug without dashes or spaces. Used to name your repo
    and in other places where a Python-importable version of your project name
    is needed.

description:
    Describes your project and gets used in places like ``README.rst`` and such.

author_name:
    This is you! The value goes into places like ``LICENSE`` and such.

email:
    The email address you want to identify yourself in the project.

domain_name:
    The domain name you plan to use for your project once it goes live.
    Note that it can be safely changed later on whenever you need to.

version:
    The version of the project at its inception.

open_source_license:
    A software license for the project. The choices are:

    1. MIT_
    2. BSD_
    3. GPLv3_
    4. `Apache Software License 2.0`_
    5. Not open source

timezone:
    The value to be used for the ``TIME_ZONE`` setting of the project.


cloud_provider:
    Select a cloud provider for static & media files. The choices are:

    1. AWS_
    2. Azure
    3. GCP_
    4. None

    Note that if you choose no cloud provider, media files won't work.


use_compressor:
    Indicates whether the project should be configured to use `Django Compressor`_.

use_celery:
    Indicates whether the project should be configured to use Celery_.

use_mailhog:
    Indicates whether the project should be configured to use MailHog_.

use_sentry:
    Indicates whether the project should be configured to use Sentry_.

use_whitenoise:
    Indicates whether the project should be configured to use WhiteNoise_.

use_travisci:
    Indicates whether the project should be configured to use `Travis CI`_.

.. _MIT: https://opensource.org/licenses/MIT
.. _BSD: https://opensource.org/licenses/BSD-3-Clause
.. _GPLv3: https://www.gnu.org/licenses/gpl.html
.. _Apache Software License 2.0: http://www.apache.org/licenses/LICENSE-2.0

.. _PyCharm: https://www.jetbrains.com/pycharm/

.. _Docker: https://github.com/docker/docker
.. _Docker Compose: https://docs.docker.com/compose/

.. _PostgreSQL: https://www.postgresql.org/docs/

.. _Gulp: https://github.com/gulpjs/gulp

.. _AWS: https://aws.amazon.com/s3/
.. _GCP: https://cloud.google.com/storage/

.. _Django Compressor: https://github.com/django-compressor/django-compressor

.. _Celery: https://github.com/celery/celery

.. _MailHog: https://github.com/mailhog/MailHog

.. _Sentry: https://github.com/getsentry/sentry

.. _WhiteNoise: https://github.com/evansd/whitenoise

.. _Heroku: https://github.com/heroku/heroku-buildpack-python

.. _Travis CI: https://travis-ci.org/
